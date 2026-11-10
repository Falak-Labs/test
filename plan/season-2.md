# Build-It — Season 2 plan (Episodes 6–20) and the new format

Written Nov 10 2026. Season 1 (Episodes 1–5, old look) is live in English. From Episode 6 on, every episode uses
the new format below. Target: 15 new episodes, each in English and Saudi Arabic = 30 videos.

## 1. The new format (v2)

**What stays:** the story. You build the simplest version, it breaks four times, you fix it four times, the narrator
says "congrats, you just built X" at both ends, a fake pause asks for the follow, and a joke closes the video.
14 lines, 65–70 seconds, 1080×1920, one cut for TikTok, YouTube Shorts and Instagram Reels.

**What changed: the look.**
- **Light instead of flat colour.** Twilight and night skies with gradients, stars, a moon, glowing lamps and light
  cones, fire and sparks that actually light the scene, then bloom, fine grain and a soft vignette on every frame.
- **Volume.** Hero objects are shaded like real cylinders and boxes (lit side, shadow side, rim light), with panel
  lines and small details. Smoke, clouds and explosions are soft and billowy, never flat circles.
- **Depth.** Far mountains and city lights, mid-ground set, the machine, then the cutaway under the ground with
  pipes and cables that glow when they carry something.
- **One palette per episode** on a dark base, with one warm accent. Rocket: navy and violet with flame orange.

**What changed: the screen language.**
- **Progress bar** at the top: build number, the name, and four segments. A segment pulses red when something
  breaks and fills green when it is fixed, so viewers always know how far along they are.
- **Captions** show two or three words at a time; the word being spoken lights up yellow and pops.
- **Labels** point at parts with a thin line and a dark glass card; a pulsing dot marks the part.
- **Badges:** a red alert with rings for every break, a green tick with a burst for every fix.
- **Whip cuts** between sets (ground, close-up, far away) instead of one long camera move.
- **The crew:** three small engineers in yellow hard hats appear in every episode. They cheer, point, duck and end
  up covered in soot. They are the running joke and the link to the channel's mascot.

**More humour, by rule:** one visual gag in every break (the crew reacts), one line in the script that is a joke
with a true fact inside it, and the closing joke must be something real (a real ship name, a real toilet in a moat).

**Arabic version:** same picture, Saudi script and voice, right-to-left progress bar and captions, green accent
where the English uses teal. Jokes are adapted, not translated (example: the race-car champagne becomes the
rose-water spray used at the Gulf races).

**Under the hood:** `kit/bik/v2.py` holds the look (sky, stars, moon, ridges, clouds, smoke, fire, explosions,
glows, shading, progress bar, labels, badges, captions, finishing pass). `kit/episodes/rocket.py` is the reference
episode. A full episode renders in about 18 minutes on two cores. Checks before anything ships: 61–70 s,
-14 LUFS, peak under -1 dB, the words still clear in the final mix, and a look at one frame per beat.

## 2. The 15 episodes

Order matters: each episode's follow line names the next one.

| # | Build | World | Why people will watch | Closing joke |
|---|---|---|---|---|
| 6 | Rocket that lands itself 🚀 | Space | Explosions, then a perfect landing | The landing ship's real name |
| 7 | Castle 🏰 | History | Attackers fail four different ways | The toilet empties into the moat |
| 8 | Claw machine 🕹️ | Arcade | "Is it rigged?" Everyone has lost to one | The giant teddy bear nobody wins |
| 9 | Submarine 🌊 | Ocean | Pressure, darkness, running out of air | The screen door |
| 10 | Toilet 🚽 | Home | Everyone uses one, nobody knows how it works | Seat up or down |
| 11 | Airplane ✈️ | Sky | A bus with wings driven off a cliff | Whose armrest is it |
| 12 | Fireworks show 🎆 | Night sky | The best-looking episode in the new style | The dog under the bed |
| 13 | Bank vault 🏦 | Heist | One thief, four failed attempts | The pen on a chain |
| 14 | Air conditioner ❄️ | Home | Summer; huge for the Arabic channel | Dad and the open door |
| 15 | Space station 🛰️ | Space | Recycled pee and the space toilet | The toilet with a seat belt |
| 16 | Suspension bridge 🌉 | City | The bridge that twisted in the wind | The paint job never ends |
| 17 | Vending machine 🥤 | Everyday | The snack that gets stuck | Slot B4, stuck since Tuesday |
| 18 | Metro 🚇 | City | Trains with no driver; Riyadh Metro for Arabic | The guy holding the doors |
| 19 | Hydroelectric dam ⚡ | Nature | A wall holding back a lake | Fish taking the stairs |
| 20 | Race car 🏎️ | Speed | Brakes at a thousand degrees, two-second pit stops | They spray the drink instead of drinking it |

Mix: space ×2, home ×2, city ×2, plus ocean, history, arcade, sky, spectacle, heist, everyday, nature, speed. No two
neighbours come from the same world.

## 3. How the 30 videos get made

For every episode, in this order:
1. Script check: every fact in the lines below is re-checked against a source before recording.
2. English voice, then the Saudi script (adapted, same 14 beats).
3. Animation in the new style, built from the rocket episode's parts; frames reviewed beat by beat.
4. English render and checks. Stored in the repo, not posted.
5. Saudi voice, Saudi render and checks.
6. Titles, captions and hashtags in both languages, queued for the posting schedule.

Pace: each episode is a few hours of animation work. Episode 6 first (its opening is already done), then down the
list. Posting pace once five are in stock: one new episode a day per language, English at 7 PM New York, Arabic at
9 PM Riyadh.

## 4. Growing the pages

What we already do: keyword-first titles, a question in every caption, a follow line that names the next build,
3–5 hashtags per app, fixed posting times, both languages cross-linked in the bios.

What we add in Season 2:
- **A daily rhythm.** One episode a day per language, same hour, no gaps. Regular posting matters more than bursts.
- **The first two seconds.** Every episode opens on the machine already moving, with the hook line on screen.
- **Reasons to comment.** Each episode ends on a real argument (seat up or down, whose armrest, is the claw rigged).
- **Reply fast.** Answers to comments in the first hour count the most. I can draft replies for you to paste.
- **Local episodes for Arabic.** The air conditioner and the Riyadh Metro go first on the Arabic channel's promo.
- **Long videos on YouTube.** After every 10 episodes, a 10-minute compilation. Long videos count toward watch hours.
- **A weekly look at the numbers.** Views, how much of each video people watch, follows per video. We make more of
  what wins and drop what doesn't.
- **Milestones.** TikTok pays from 10,000 followers and 100,000 views in 30 days, for videos over a minute.
  YouTube pays ads from 1,000 subscribers and 10 million Shorts views in 90 days.

## 5. The scripts (English, draft 1)

Line order in every script: hook, break 1, fix 1, break 2, fix 2, break 3, fix 3, break 4, fix 4, follow line,
reveal, three numbers, closer, joke.

### Ep 6 — Rocket that lands itself (kit: rocket)
1. If you launch a rocket and just wait, congrats, you just built a rocket that lands itself.
2. But it comes down nose first, faster than a bullet, and turns your launch pad into a crater.
3. So you add gas thrusters that flip it around, and relight the engines to brake, so it falls tail first.
4. Now it's slower, until the air grabs it, and it starts to tumble like a dropped pencil.
5. So you add four grid fins near the top, like flying waffle irons, that steer it all the way down.
6. But the engine is too strong: even on its lowest setting, it pushes the empty rocket back up.
7. So it can't hover. You time one last burn, so the speed hits zero at the exact moment it touches the ground.
8. Now it touches down softly, but it's as tall as a fourteen-story building, and it tips right over.
9. So you add four legs that fold out wide just before landing, with crush cores inside that soak up the hit.
10. But before you start the countdown, follow, because next we're building a castle.
11. Now just park a ship in the ocean, paint a target on the deck, and land on that.
12. One rocket, nine engines, zero pilots.
13. And congrats, you just built a self-landing rocket yourself.
14. And the ship's name? "Of Course I Still Love You." Even engineers have feelings.

### Ep 7 — Castle (kit: castle)
1. If you pile up a hill of dirt and put your house on top, congrats, you just built a castle.
2. But the neighbors show up with torches, and your wooden walls burn like firewood.
3. So you rebuild in stone, with walls thicker than a car is long, and round towers that boulders glance off.
4. Now it won't burn, until they bring ladders and simply climb over.
5. So you dig a moat all the way around, and top the walls with stone teeth: gaps to shoot from, blocks to hide behind.
6. But the front door is still a door, and they brought a battering ram.
7. So you add a drawbridge, an iron gate that drops like a guillotine, and holes in the ceiling for hot surprises.
8. Now nobody gets in, and neither does lunch: they just camp outside and wait for you to starve.
9. So you dig a well inside the walls, store a year of grain, and add a secret back door for midnight raids.
10. But before you raise the flag, follow, because next we're building a claw machine.
11. Now just hang some banners, light the torches, and hire one guy with a trumpet.
12. One hill, four towers, zero visitors.
13. And congrats, you just built a castle yourself.
14. And the toilet? A hole in the wall, straight into the moat. That's why nobody swims in the moat.

### Ep 8 — Claw machine (kit: claw)
1. If you hang a claw over a box of toys, congrats, you just built a claw machine.
2. But the claw grabs too well, and one kid empties the whole box with a single coin.
3. So you add a dial inside that sets the grip: strong enough to lift a prize, weak enough to drop it halfway.
4. Now nobody ever wins, so nobody ever plays.
5. So you add a small computer that counts the coins, and lets the claw squeeze tight once in a while.
6. But kids learn to rock the machine until the prizes fall into the chute.
7. So you bolt it to the floor, and add a tilt sensor with an alarm loud enough to embarrass anyone.
8. Now it's safe, until a kid climbs in through the prize door. Yes, that really happens.
9. So you add a one-way flap on the chute, and a light beam that knows when a prize, and only a prize, drops.
10. But before you drop a coin, follow, because next we're building a submarine.
11. Now just add flashing lights, a song that never stops, and one giant teddy bear nobody can lift.
12. One claw, a hundred toys, zero winners.
13. And congrats, you just built a claw machine yourself.
14. And the giant teddy bear? He's been in there since 2009. He lives there now.

### Ep 9 — Submarine (kit: submarine)
1. If you seal yourself in a barrel and roll into the sea, congrats, you just built a submarine.
2. But it floats like a cork, and you just bob around, waving at seagulls.
3. So you add ballast tanks: let seawater in to sink, and blow it out with compressed air to rise.
4. Now you can dive, until the deep water squeezes your barrel like a soda can.
5. So you build the hull as a thick steel tube with rounded ends, the shape that spreads the squeeze evenly.
6. But down there it's pitch black, and you just drove into a mountain.
7. So you add sonar that bounces sound off everything around you, and a periscope for a peek at the surface.
8. Now you can find your way, until the air goes stale and the whole crew starts yawning.
9. So you add scrubbers that pull out the carbon dioxide, and a machine that makes fresh oxygen out of water.
10. But before you dive, follow, because next we're building a toilet.
11. Now just add a propeller, paint it black, and tell nobody where you parked it.
12. One hull, a hundred sailors, zero windows.
13. And congrats, you just built a submarine yourself.
14. And the screen door? Still a bad idea.

### Ep 10 — Toilet (kit: toilet)
1. If you put a seat over a bucket, congrats, you just built a toilet.
2. But somebody has to carry the bucket, and nobody wants that job.
3. So you add a tank of water above the bowl, with a rubber flap at the bottom: push the handle, and gravity does the dirty work.
4. Now it flushes, until the sewer sends its smell back up to say hello.
5. So you bend the pipe into an S, so a little water always stays in the curve and blocks the gas.
6. But the tank keeps filling forever, and now your bathroom is a swimming pool.
7. So you add a float that rises with the water and shuts the valve when the tank is full, plus an overflow tube, just in case.
8. Now it works, until the flush goes glug, glug, and stalls halfway.
9. So you run a vent pipe up through the roof, so air can follow the water down, and everything flows.
10. But before you sit down, follow, because next we're building an airplane.
11. Now just add a lid, a lock on the door, and a magazine from 2014.
12. One push, six liters, zero buckets.
13. And congrats, you just built a toilet yourself.
14. And the seat? Up or down? Engineers are still working on that one.

### Ep 11 — Airplane (kit: airplane)
1. If you glue wings on a bus and drive it off a cliff, congrats, you just built an airplane.
2. But flat wings don't lift anything, so it's just a bus, falling, with extra steps.
3. So you curve the wings and tilt them into the wind, so they push air down and the air pushes them up, and add engines to keep it coming.
4. Now it flies, until you climb where the air is thin, and everybody on board takes a nap.
5. So you seal the cabin and pump it full of air, like a soda can with seats.
6. But it wobbles and rolls like a paper plane with a bent wing.
7. So you add a tail with a rudder, and small hinged flaps on the wings and tail that tilt the plane any way you want.
8. Now it goes where you point it, until it's time to land, at twice highway speed, with nowhere to stop.
9. So you add big flaps to fly slower, wheels with shock absorbers, and engines that blow their air forward to brake.
10. But before you fasten your seatbelt, follow, because next we're building a fireworks show.
11. Now just add tiny windows, tiny pretzels, and a seat that leans back exactly one inch.
12. Two wings, three hundred seats, zero legroom.
13. And congrats, you just built an airplane yourself.
14. And the armrest in the middle? Nobody knows whose it is. Science has no answer.

### Ep 12 — Fireworks show (kit: fireworks)
1. If you set off a bag of gunpowder in your backyard, congrats, you just built a fireworks show.
2. But it goes boom on the ground, and now you don't have a fence. Or eyebrows.
3. So the pros pack it into a shell, drop it in a steel tube, and put a lift charge underneath that shoots it into the sky.
4. Now it flies, until it bursts too early, right above everyone's head.
5. So they add a time fuse that burns on the way up, and sets off the burst at the very top.
6. But it's just a white flash and a bang: no color, no shape, no "ooooh".
7. So they fill the shell with pellets called stars, with metals inside: strontium burns red, barium green, copper blue.
8. Now it's beautiful, until someone has to run between a hundred tubes with a lighter.
9. So they wire every shell to a computer that fires them from far away, exactly on the beat of the music.
10. But before you look up, follow, because next we're building a bank vault.
11. Now just add music, a crowd on blankets, and one guy who claps too early.
12. One button, a thousand shells, zero eyebrows lost.
13. And congrats, you just built a fireworks show yourself.
14. And the dog? Under the bed until Tuesday.

### Ep 13 — Bank vault (kit: vault)
1. If you put your money in a box and lock it, congrats, you just built a bank vault.
2. But a thief just picks up the box and walks away.
3. So you make the box a whole room, with walls of concrete and steel as thick as your arm is long.
4. Now it can't walk off, until he comes back with a drill and goes straight for the lock.
5. So you hide a sheet of glass inside the door: if a drill cracks it, extra bolts snap shut, and even the right code won't open it.
6. But then he skips the drill, and makes the manager open it at midnight.
7. So you add a time lock, a clock inside the door that keeps it shut until morning, no matter who asks.
8. Now he's stuck outside, so he starts digging a tunnel under the floor.
9. So you add sensors that feel the tiniest shake and hear the quietest scratch, and call the police before he's through.
10. But before you spin the wheel, follow, because next we're building an air conditioner.
11. Now just add a giant round door, a shiny wheel, and a pen on a chain, so nobody steals the pen.
12. One door, twenty bolts, zero heists.
13. And congrats, you just built a bank vault yourself.
14. And the pen? Stolen on day one.

### Ep 14 — Air conditioner (kit: aircon)
1. If you put a block of ice in front of a fan, congrats, you just built an air conditioner.
2. But the ice melts in an hour, and now you have a puddle and a warm fan.
3. So you swap the ice for a special liquid that boils inside a cold coil, and drinks up the heat from your room.
4. Now the room cools down, until the liquid is all gas, full of heat, with nowhere to put it.
5. So you add a compressor that squeezes the gas, and a second coil outside with a fan that dumps the heat on the street.
6. But it never stops, and now your living room is a penguin habitat.
7. So you add a thermostat that switches it off at the temperature you pick, and back on when it warms up.
8. Now it's perfect, until water starts dripping out of the wall, onto your couch.
9. So you add a tray and a drain pipe for the water it pulls out of the air, and a filter that catches the dust.
10. But before you grab the remote, follow, because next we're building a space station.
11. Now just hide half of it outside, hang the other half on the wall, and lose the remote.
12. One room, two coils, zero sweat.
13. And congrats, you just built an air conditioner yourself.
14. And your dad? "Close the door! I'm not cooling the whole street!"

### Ep 15 — Space station (kit: station)
1. If you seal a room and throw it into orbit, congrats, you just built a space station.
2. But the air inside runs out before the weekend.
3. So you add a machine that splits water into oxygen, and filters that scrub out the carbon dioxide.
4. Now you can breathe, until the water runs out, and the nearest store is four hundred kilometers straight down.
5. So you recycle everything: sweat, breath, and yes, pee. Yesterday's coffee is tomorrow's coffee.
6. But nothing weighs anything up there, and your muscles and bones slowly waste away.
7. So you add a treadmill with bungee straps and a weightlifting machine, and everyone works out two hours a day.
8. Now you're healthy, until a speck of paint hits the wall at twenty-eight thousand kilometers an hour.
9. So you wrap the station in layered shields that shatter the speck before it reaches the hull, and add solar wings for power.
10. But before you float away, follow, because next we're building a suspension bridge.
11. Now just add a big window facing Earth, and Velcro on absolutely everything.
12. One station, sixteen sunrises a day, zero showers.
13. And congrats, you just built a space station yourself.
14. And the toilet? It's a vacuum cleaner with a seat belt. Aim carefully.

### Ep 16 — Suspension bridge (kit: bridge)
1. If you lay a plank across a river, congrats, you just built a bridge.
2. But the river is a mile wide, and your plank sags and snaps in the middle.
3. So you build two tall towers, and hang the road from giant cables draped over them, like laundry on a clothesline.
4. Now it hangs, until the weight of the road drags the cable ends right out of the ground.
5. So you tie each end into a block of concrete as big as a building, buried in the riverbank.
6. But then the wind makes the road twist and gallop like a ribbon.
7. So you stiffen the deck with a steel frame, and shape its edges like a wing, so the wind slides past.
8. Now it's steady, until a hot summer day makes the steel grow, and the road buckles.
9. So you leave gaps in the road, with steel teeth that slide in and out, and let the whole bridge breathe.
10. But before you cut the ribbon, follow, because next we're building a vending machine.
11. Now just paint it bright orange, and then paint it again, forever.
12. One river, two towers, fifty thousand wires.
13. And congrats, you just built a suspension bridge yourself.
14. And the painting? It never ends. There's always one more rust spot.

### Ep 17 — Vending machine (kit: vending)
1. If you leave snacks on a shelf with a jar for the money, congrats, you just built a vending machine.
2. But people take the snacks. And the jar.
3. So you lock everything behind glass, and add a coin slot that weighs and measures every coin, and spits out the fakes.
4. Now it gets paid, until it has to hand over a snack without opening the door.
5. So you sit every snack in a metal spiral: a motor turns it once, and the snack walks to the edge and drops.
6. But the chips get stuck, hanging by one corner, mocking you.
7. So you add a light beam at the bottom: if nothing falls through it, the spiral turns again, or you get your money back.
8. Now it's fair, until someone tips the whole machine to shake the snacks loose.
9. So you bolt it down, add a flap so no arm fits up the slot, and an alarm that screams when it tilts.
10. But before you pick a snack, follow, because next we're building a metro.
11. Now just add a glowing front, a loud hum, and the one snack nobody ever buys.
12. One machine, forty snacks, zero cashiers.
13. And congrats, you just built a vending machine yourself.
14. And B4? Stuck since Tuesday. Everyone can see it. Nobody can have it.

### Ep 18 — Metro (kit: metro)
1. If you dig a tunnel and push a wagon through it, congrats, you just built a metro.
2. But pushing is slow, and an engine would fill the tunnel with smoke.
3. So you run it on electricity, from a third rail beside the track: no smoke, no fuel tank.
4. Now it's fast, until one train catches up with another in the dark.
5. So you add a computer that knows where every train is and keeps a safe gap between them. It's so good, you don't need a driver.
6. But on a crowded platform, somebody always stands too close to the edge.
7. So you add glass doors along the platform, that only open when a train has stopped right behind them.
8. Now it's safe, until a train stops between stations, and it gets hot and stuffy.
9. So you add giant fans, vent shafts up to the street, and a lit walkway along the wall to the next station.
10. But before you tap your card, follow, because next we're building a dam.
11. Now just add a map with colored lines, and a calm voice that says "mind the gap".
12. One tunnel, a train every two minutes, zero drivers.
13. And congrats, you just built a metro yourself.
14. And the guy holding the doors? He adds four minutes to everyone's day. Every day.

### Ep 19 — Hydroelectric dam (kit: dam)
1. If you block a river with a pile of rocks, congrats, you just built a dam.
2. But the lake behind it gets heavier every day, and shoves your pile downstream.
3. So you build it in concrete, thickest at the bottom where the push is strongest, and curved like an arch, to lean on the canyon walls.
4. Now it holds, but all that water is just sitting there, doing nothing.
5. So you run pipes through the wall, and the falling water spins turbines that turn generators. That's electricity.
6. But then a storm fills the lake to the brim, and the water starts pouring over the top.
7. So you add spillways: giant gates and slides that let the extra water out before it overflows.
8. Now it's safe, until the fish show up for their trip upstream, and hit a wall.
9. So you build a fish ladder: a staircase of little pools they can jump up, one step at a time.
10. But before you flip the switch, follow, because next we're building a race car.
11. Now just add power lines, a road across the top, and a gift shop.
12. One wall, seventeen turbines, a million homes.
13. And congrats, you just built a dam yourself.
14. And the fish? Still taking the stairs. No elevator. We checked.

### Ep 20 — Race car (kit: racecar)
1. If you bolt a huge engine onto a go-kart, congrats, you just built a race car.
2. But at the first fast corner, it slides straight off the track.
3. So you add wings, upside down: instead of lifting the car, the air squashes it onto the road.
4. Now it sticks, until you brake from three hundred, and the brakes catch fire.
5. So you fit brake discs made of carbon, the kind that work best glowing red, at a thousand degrees.
6. But the tires wear out before the race is half done.
7. So you train a crew of twenty to change all four in about two seconds.
8. Now it's fast everywhere, until it meets a wall.
9. So you build a carbon-fiber shell around the driver, a titanium ring over his head, and a nose that crumples so he doesn't.
10. But before you start your engine, follow, because next we're building a cruise ship.
11. Now just cover it in stickers, and add a steering wheel with thirty buttons.
12. One driver, a thousand horsepower, zero cup holders.
13. And congrats, you just built a race car yourself.
14. And the winner's drink? They don't even drink it. They spray it. On purpose.
