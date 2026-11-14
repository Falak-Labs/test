"""Tiny Buffer GraphQL client (https://developers.buffer.com). It reads the schema at run time (introspection), so
small changes in Buffer's beta API (type names, enum values, union members) don't break the posting run."""
import datetime as dt
import json
import os
import time

import requests

API = "https://api.buffer.com"
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state", "buffer-schema.json")
CACHE_DAYS = 3      # the schema is re-read after this many days (it costs ~15 of the 3,000 monthly API requests)
TYPE_REF = "kind name ofType { kind name ofType { kind name ofType { kind name } } }"


def unwrap(t):
    while t and t.get("ofType") and t["kind"] in ("NON_NULL", "LIST"):
        t = t["ofType"]
    return t


class BufferError(RuntimeError):
    pass


def _load_cache():
    try:
        d = json.load(open(CACHE, encoding="utf-8"))
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(d["saved"])
        return d["types"] if age < dt.timedelta(days=CACHE_DAYS) else {}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


class Buffer:
    _schema = None          # the API schema is the same for every account: one cache per process, saved in state/
    quota = {}              # label -> the rate-limit header Buffer sent last (what is left of the API allowance)

    def __init__(self, key, label=""):
        self.key, self.label = key, label
        if Buffer._schema is None:
            Buffer._schema = _load_cache()
        self._types = Buffer._schema
        self.calls = 0

    # ------------------------------------------------------------------ transport
    def q(self, query, variables=None):
        for attempt in range(5):
            r = requests.post(API, json={"query": query, "variables": variables or {}}, timeout=90,
                              headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"})
            self.calls += 1
            seen = [f"{hk}={hv}" for hk, hv in r.headers.items() if "ratelimit" in hk.lower() and "reset" not in hk.lower()]
            if seen:
                Buffer.quota[self.label] = "; ".join(seen)[:300]
            if r.status_code == 429 or r.status_code >= 500:
                wait = int(r.headers.get("Retry-After", "0") or 0) or 10 * (attempt + 1)
                if r.status_code == 429 and wait > 900:
                    raise BufferError(f"Buffer API allowance used up; it frees up in about {wait // 3600 + 1} h")
                print(f"  [{self.label}] Buffer {r.status_code}, retrying in {wait}s")
                time.sleep(min(wait, 120))
                continue
            if r.status_code == 401:
                raise BufferError("Buffer refused the API key (401): check the BUFFER_KEY secret")
            r.raise_for_status()
            js = r.json()
            if js.get("errors"):
                raise BufferError(json.dumps(js["errors"], ensure_ascii=False)[:1200])
            return js["data"]
        raise BufferError("Buffer kept answering 429/5xx")

    # ------------------------------------------------------------------ schema
    def type(self, name):
        if name not in self._types:
            d = self.q("query($n: String!) { __type(name: $n) { kind name "
                       "fields { name type { " + TYPE_REF + " } args { name type { " + TYPE_REF + " } } } "
                       "inputFields { name type { " + TYPE_REF + " } } enumValues { name } "
                       "possibleTypes { name } } }", {"n": name})
            self._types[name] = d["__type"] or {}
            try:
                os.makedirs(os.path.dirname(CACHE), exist_ok=True)
                with open(CACHE, "w", encoding="utf-8") as f:
                    json.dump({"saved": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "types": self._types}, f)
            except OSError:
                pass
        return self._types[name]

    def field(self, type_name, field_name):
        for f in self.type(type_name).get("fields") or []:
            if f["name"] == field_name:
                return f
        return None

    def input_field(self, type_name, field_name):
        for f in self.type(type_name).get("inputFields") or []:
            if f["name"] == field_name:
                return f
        return None

    def enum_values(self, name):
        return [e["name"] for e in self.type(name).get("enumValues") or []]

    def selection(self, type_name, wanted, depth=0):
        """Selection set with the wanted fields that exist; object fields get their scalar sub-fields."""
        out = []
        for f in self.type(type_name).get("fields") or []:
            if wanted and f["name"] not in wanted:
                continue
            t = unwrap(f["type"])
            if any(a for a in f.get("args") or [] if a["type"]["kind"] == "NON_NULL"):
                continue
            if t["kind"] in ("SCALAR", "ENUM"):
                out.append(f["name"])
            elif t["kind"] == "OBJECT" and depth == 0:
                sub = self.selection(t["name"], None, depth + 1)
                if sub:
                    out.append(f["name"] + " { " + sub + " }")
        return " ".join(out)

    # ------------------------------------------------------------------ data
    def organizations(self):
        return self.q("query { account { organizations { id name } } }")["account"]["organizations"]

    def channels(self):
        out = []
        for org in self.organizations():
            d = self.q('query { channels(input: { organizationId: "%s" }) { id name displayName service isQueuePaused } }'
                       % org["id"])
            for ch in d["channels"]:
                ch["organizationId"] = org["id"]
                out.append(ch)
        return out

    def create_post(self, inp, mutation="createPost"):
        mf = self.field("Mutation", mutation)
        arg = next(a for a in mf["args"] if a["name"] == "input")
        in_type = unwrap(arg["type"])["name"]
        ret = unwrap(mf["type"])["name"]
        post_sel = self.selection("Post", {"id", "status", "dueAt", "sentAt", "externalLink", "serviceLink"})
        frags = []
        members = [p["name"] for p in self.type(ret).get("possibleTypes") or []] or [ret]
        for m in members:
            names = {f["name"] for f in self.type(m).get("fields") or []}
            if "post" in names:
                frags.append("... on %s { post { %s } }" % (m, post_sel))
            elif "message" in names:
                frags.append("... on %s { message }" % m)
        d = self.q("mutation($input: %s!) { %s(input: $input) { __typename %s } }" % (in_type, mutation, " ".join(frags)),
                   {"input": inp})[mutation]
        if d.get("post"):
            return d["post"]
        raise BufferError(d.get("message") or json.dumps(d, ensure_ascii=False))

    def edit_post(self, inp):
        """editPost takes the same fields as createPost plus the post id; returns the post."""
        return self.create_post(inp, mutation="editPost")

    def posts(self, organization_id, statuses, extra=()):
        pf = self.field("Query", "posts")
        in_type = unwrap(next(a for a in pf["args"] if a["name"] == "input")["type"])["name"]
        filt = self.input_field(in_type, "filter")
        status_enum = None
        if filt:
            sf = self.input_field(unwrap(filt["type"])["name"], "status")
            status_enum = unwrap(sf["type"])["name"] if sf else None
        ok = set(self.enum_values(status_enum)) if status_enum else set()
        statuses = [s for s in statuses if s in ok] if ok else statuses
        conn = unwrap(pf["type"])["name"]
        edges = self.field(conn, "edges")
        node_type = unwrap(self.field(unwrap(edges["type"])["name"], "node")["type"])["name"]
        sel = self.selection(node_type, {"id", "status", "dueAt", "sentAt", "createdAt", "channelId", "channelService",
                                         "text", "externalLink", "serviceLink", "error", "errorMessage", "channel"}
                             | set(extra))
        # Buffer pages its results (10 by default): ask for bigger pages and follow the cursor.
        top = {a["name"] for a in pf["args"]}
        inner = {f["name"] for f in self.type(in_type).get("inputFields") or []}
        page_info = self.field(conn, "pageInfo")
        pi_fields = {f["name"] for f in self.type(unwrap(page_info["type"])["name"]).get("fields") or []} if page_info else set()
        page_sel = " pageInfo { hasNextPage endCursor }" if {"hasNextPage", "endCursor"} <= pi_fields else ""
        out, after = [], None
        for _ in range(40):
            inp_extra, top_extra = "", ""
            for name, val in (("first", "25"), ("after", '"%s"' % after if after else None)):
                if val is None:
                    continue
                if name in top:
                    top_extra += ", %s: %s" % (name, val)
                elif name in inner:
                    inp_extra += ", %s: %s" % (name, val)
            q = ('query { posts(input: { organizationId: "%s", filter: { status: [%s] }%s }%s) { edges { node { %s } }%s } }'
                 % (organization_id, ", ".join(statuses), inp_extra, top_extra, sel, page_sel))
            d = self.q(q)["posts"]
            out += [e["node"] for e in d.get("edges") or []]
            pi = d.get("pageInfo") or {}
            if not (pi.get("hasNextPage") and pi.get("endCursor") and ("after" in top or "after" in inner)):
                break
            after = pi["endCursor"]
        return out