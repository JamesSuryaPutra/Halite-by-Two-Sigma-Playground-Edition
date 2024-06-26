# Halite by Two Sigma: Playground Edition
![header](https://github.com/JamesSuryaPutra/Halite-by-Two-Sigma-Playground-Edition/assets/155945814/efdd1b72-4230-4733-83ac-16e52462acf0)

# Description
Note:
This simulation is a playground competition extending the fourth season of Halite for participation. We have modified the rules to serve as a two-player game instead of four-player game. No points or medals will be awarded for this competition.

Ahoy there! There's halite to be had and ships to be deployed! Are you ready to navigate the skies and secure your territory?

Halite by Two Sigma ("Halite") is a resource management game where you build and control a small armada of ships. Your algorithms determine their movements to collect halite, a luminous energy source. The most halite at the end of the match wins, but it's up to you to figure out how to make effective and efficient moves. You control your fleet, build new ships, create shipyards, and mine the regenerating halite on the game board.

Created by Two Sigma in 2016, more than 15,000 people around the world have participated in a Halite challenge. Players apply advanced algorithms in a dynamic, open source game setting. The strategic depth and immersive, interactive nature of Halite games make each challenge a unique learning environment.

Halite IV builds on the core game design of Halite III with a number of key changes that shift the focus of the game towards tighter competition on a smaller board. New game features include regenerating halite, shipyard creation, no more ship movement costs, and stealing halite from other players!

So dust off your halite meters and fasten your seatbelts. The fourth season of Halite is about to begin!

# Halite rules
Note:
The environment rules for the playground version of Halite IV are the same as the featured version, except the playground environment is for two players instead of four, and the turn timeout has been reduced to 3 seconds from 6 seconds.

### Rules
In this game, you control a small armada of spaceships, mining the rare mineral “halite” from the depths of space and teleporting it back to your home world. But it turns out you aren’t the only civilization with this goal; in each game 2 opponents will compete to collect the most halite from the board. Whoever collects the most halite by the end of 400 turns, or eliminates all of their opponents from the board before that, will be the winner!

### Summary
- The player with the most halite at the end of the game wins.
- You start the game with 1 ship and 5,000 halite.
- Converting a ship to a shipyard costs 500 halite.
- Spawning a ship from a shipyard costs 500 halite.
- Each turn you can issue one command to each ship you control to go North, South, East, West, or to convert into a shipyard.
- If a ship is not issued a command it will not move and will instead mine 25% of the halite underneath its current position. Mined halite is stored on the ship, and there is no maximum to how much halite a ship can hold.
- Halite on ships cannot be spent to buy ships or shipyards until deposited at a shipyard (with a specific exception detailed under the convert section below). At the end of the game - players need to move their ships over shipyards to deposit the halite and teleport it back to their homeworlds to count for the final Halite total.
- Ships that move onto the same square collide. The smallest ship (that is, the one with the least halite in its storage) survives and all other ships will be destroyed. The smallest ship steals all of the halite from other ships it collides with. If two or more ships have tie for the smallest amount of halite they are both destroyed. After ship collision a check is performed for a shipyard collision, if an enemy ship collides with a shipyard both are destroyed.
- If a player loses all of their ships and shipyards they are eliminated from the game.
- Halite is distributed randomly (but symmetrically) at the start of the game.
- Halite in each cell regenerates by 2% per turn, up to a maximum of 500 halite.
- The game lasts a maximum of 400 turns.

### Game setup
- At the start of the game, each player is assigned a random color and mirrored location on the game board. Each player starts with 1 ship and 5,000 halite.
- The game board is 21x21 cells large and wraps around on both the north/south and east/west border. The southwest (bottom-left) corner of the board is designated (0,0) and the northeast (top-right) corner of the board is designated (20,20). The starting player positions are at (5,10) and (15,10). In the game code positions are given as serialized list where each cell is an integer calculated by the formula: [position = row * 21 + column].
- The map is covered with a random distribution of halite. This distribution is symmetric both vertically and horizontally. Each cell has no more than 500 halite (the maximum amount a cell can have). In total the game board starts with 24,000 halite on it. In the visualizer the size of the halite icon is proportional to the amount of halite on that square.

### Strategy tip
You will notice that players do not start with a shipyard, this means the first decision a player needs to make is where to create their first one. Many players will want to convert their starting ship to a shipyard on the first turn so they can create more ships ASAP.

### Turn order
- Each game of Halite lasts for 400 turns or until all but one player has been eliminated. Each turn each agent will be given a copy of the board state (the “observation”) with complete information about every aspect of the game (including how much halite each player has, the position of all ships (and how much halite they have one them) and how much halite is on every cell of the board. Each agent will then need to return a list of actions for their ships and shipyards to take within a set amount of time.
- If your agent does not return actions in time or encounters and error, it will be marked as errored and will immediately have all of its ships and shipyards removed from the game. This will place the player last in final score order (behind even players who had been previously eliminated).
- Each turn each ship can make one of the following actions:
  - Move
    - Actions: NORTH, SOUTH, EAST, WEST
    - Cost: 0 halite
    - This action will move a ship one space in the requested direction. If multiple ships end their turn in the same space collision will happen (more on that below). If a ship 
    travels onto a friendly shipyard it will instantly deposit any halite it was carrying, teleporting it to the player’s homeworld (adding it to the players total halite). Note that 
    halite depositing is resolved after collision. Please note that unlike Halite III, in this game it costs no halite for ships to move.
  - Hold / Mine
    - Actions: N/A
    - Cost: 0 halite
    - If a ship is not issued an order for a turn it will hold its current position without moving. It will also mine the halite from the cell it is on whenever it does this. Ships mine 
    25% of the total halite of a cell each turn they are on top of that cell. Mined halite is added to that individual ship’s storage and will need to be deposited at a shipyard to count 
    towards the end of game scoring. Note that collision is resolved before mining.
  - Convert
    - Actions: CONVERT
    - Cost: 500 halite
    - If a ship issues a “CONVERT” action, it will destroy itself in order to create a new shipyard on the space it is on. Conversion happens before collision during turn resolution.
    - Any halite on the cell underneath the new shipyard will be destroyed. Any halite carried by the ship converting itself will be deposited instantly. The 500 halite cost to convert a 
    ship is first subtracted from the amount the ship is holding and then whatever cost is left is removed from the players halite total. This means you can convert a ship even if you 
    have less than 500 halite, provided your total halite plus the ship’s carried halite are greater than 500 halite. If you have less than 500 halite between your halite and the halite 
    on the ship this action will fail and will be resolved as a hold move. A convert action will also fail if the ship attempting to convert is currently on top of a shipyard.
    - If you have a ship with lots of halite on it being chased/cornered by an enemy you can convert your ship to a shipyard as a way to safely deposit your halite since conversion 
    happens before collision.
- In addition to ships, each shipyard can make an action:
  - Spawn ship
    - Actions: SPAWN
    - Cost: 500 halite
    - If a shipyard issues a SPAWN command it will attempt to spawn a new ship on top of itself. A SPAWN command will only be successful if the player who issued it has sufficient halite 
    to complete the order. Spawning happens before collision, so new ships can collide with enemies (or friendly ships) and potentially be destroyed on the turn they are created.
    - It's important to avoid spawning ships when other ships are trying to deposit halite to your shipyard. If an enemy ship is about to attack your shipyard, remember that you can 
    defend it by spawning a ship to collide with theirs.
  - Hold
    - Actions: N/A
    - Cost: 0 halite
    - If no order is submitted for a shipyard it will do nothing for the turn.

### Turn resolution
After both players have submitted their actions for the turn, the system will automatically resolve the turn and update the board state. Both player turns are resolved simultaneously across the following phases:
- Spawning
  All shipyards that ordered a spawn action are resolved with new ships being added to the board on top of the shipyards that spawned them. At this phase multiple ships/shipyards can 
  occupy the same space on the board- these overlaps will be resolved in collision resolution. Spawning is resolved in board position order (top left first), which becomes relevant if a 
  player runs out of halite part way through resolving all of their spawning orders.
- Conversion
  All ships that attempted to convert into shipyards are resolved. Ships turn into shipyards if there are sufficient funds available and they are not already on top of an existing 
  shipyard. Shipyard conversions are resolved in board position order (top left first), which becomes relevant if a player runs out of halite part way through resolving all of their 
  conversion orders.
- Movement
  All ships are moved according to their orders. Note that ships are able to move “through” each other (if they each move to the other’s previous space) without colliding.
- Ship collision
  Ship collision is resolved, reducing the number of ships in every cell on the board to one or less. In each collision the smallest ship is the survivor, with all others destroyed. The 
  smallest ship is defined as the ship with the least halite in its storage. If multiple ships tie for having the least halite, all the ships in the collision are destroyed. Note that 
  collision does not consider which player owns which ships, collision between friendly ships is possible. The surviving ships takes all of the halite from the destroyed ships’ cargoes 
  and retains its place on the board.
- Shipyard collision
  If a ship and shipyard from different players occupy the same cell on the board both are destroyed. Any halite held by the ships is lost. Having your shipyard destroyed does not 
  reduce your total halite, all deposited halite has already been teleported safely back to your homeworld.
- Halite depositing
  All ships that are on top of friendly shipyards deposit all halite they have in their individual storage.
- Halite mining
  All ships that held their position on top of halite mine it, moving 25% of the cell’s halite into that ship’s storage. Halite in ship storage is indicated in the visualizer by a blue 
  glow on top of the ship.
- Halite regeneration
  Every cell on the board that has more than 0 halite and no ships on top of it will now regenerate by 2% of the existing amount of halite in the cell. Halite can grow up to a maximum 
  of 500 halite per cell.
- End turn
  The “step” number is incremented, ending the turn. The updated board is saved and redistributed to each agent as the “observation”, moving to the next turn. At this step, a player is 
  eliminated if they are no longer able to viably compete in the game. This happens when the player no longer has any ships and has less than 500 halite remaining or no remaining 
  shipyards (and thus cannot spawn any more ships). At the end of each turn the game also checks if either player has been eliminated or if the game has reached turn 400. If either of 
  those is true instead of starting a new turn the game moves to the game end step.

### Game end
When the game ends players are ranked based on their final collected halite. Ships, shipyards and undeposited halite are all worth nothing at the end of the game. Players are ranked in order of how much total halite they ended the game with. Players tied for total halite collected also tie in the game rankings. Eliminated players score 0 for total halite collected (regardless of how much halite they had when they were eliminated). Finally all bots that had errors are tied last in the rankings.

The final rankings feed into the evaluation system that then modifies each player’s Skill Rating. Check out the evaluation tab for more details.

# Basic strategies
The most straightforward way to get started with Halite is to write a bot that can convert your starting ship into a shipyard, spawn a new ship, and then travel out to collect nearby halite and return it. From there the next step is to control a group of ships (and prevent them colliding into each other).

After you get the basics down you should think about what other creative ideas you want to program. Some ideas to get you started:
- An aggressive bot that steals from your opponent or tries to eliminate them from the game.
- Defensive strategies to hold off enemy attacks.
- Efficiently controlling the board with shipyards.
- Protect high yield halite patches near your shipyard from enemies and mine them efficiently to maximize halite regeneration over the course of the game.

A more advanced alternative to programming strategies directly is to approach the problem using machine learning. In Halite III the best machine learning bot in the competition ranked #11 in the competition; can we get even better results in Halite IV?

# Evaluation
Each day your team is able to submit up to 5 agents (bots) to the competition. Each submission will play episodes (games) against other bots on the ladder that have a similar skill rating. Over time skill ratings will go up with wins or down with losses. Every bot submitted will continue to play games until the end of the competition. On the leaderboard only your best scoring bot will be shown, but you can track the progress of all of your submissions on your Submissions page.

Each Submission has an estimated Skill Rating which is modeled by a Gaussian N(μ,σ2) where μ is the estimated skill and σ represents our uncertainty of that estimate which will decrease over time.

When you upload a Submission, we first play a Validation Episode where that Submission plays against copies of itself to make sure it works properly. If the Episode fails, the Submission is marked as Error. Otherwise, we initialize the Submission with μ0=600 and it joins the pool of All Submissions for ongoing evaluation.

We repeatedly run Episodes from the pool of All Submissions, and try to pick Submissions with similar ratings for fair matches. We aim to run ~8 Episodes a day per Submission, with an additional slight rate increase for the newest-submitted Episodes to give you feedback faster.

After an Episode finishes, we'll update the Rating estimate for all Submissions in that Episode. If one Submission won, we'll increase its μ and decrease its opponent's μ -- if the result was a draw, then we'll move the two μ values closer towards their mean. The updates will have magnitude relative to the deviation from the expected result based on the previous μ values, and also relative to each Submission's uncertainty σ. We also reduce the σ terms relative to the amount of information gained by the result. The score by which your bot wins or loses an Episode does not affect the skill rating updates.

At the submission deadline, additional submissions will be locked. One additional week will be allotted to continue to run games. At the conclusion of this week, the leaderboard is final.
