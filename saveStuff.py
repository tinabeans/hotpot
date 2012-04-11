from pymongo.objectid import ObjectId

def start(db):

	'''
	db.stamps.remove();

	db.stamps.save({
		'slug' : 'awesomeness',
		'description' : 'That was amazing!',
		'name' : 'Awesomeness'
	})
	
	db.stamps.save({
		'slug' : 'aromatherapy',
		'description' : 'What a wonderful smell...',
		'name' : 'Aromatherapy'
	})
	
	db.stamps.save({
		'slug' : 'bonfire',
		'description' : 'Eep! Get the fire extinguisher!',
		'name' : 'Bonfire'
	})
	
	db.stamps.save({
		'slug' : 'madScientist',
		'description' : 'Getting a little creative here...',
		'name' : 'Mad Scientist'
	})
	
	db.stamps.save({
		'slug' : 'trueLove',
		'description' : """I... I think I'm in love.""",
		'name' : 'True Love'
	})
	
	db.stamps.save({
		'slug' : 'happyAccident',
		'description' : """Yay, that actually worked!""",
		'name' : 'Happy Accident'
	})
	'''
	
	'''
	# stamps we don't need yet...
	
	db.stamps.save({
		'slug' : 'kaboom',
		'description' : """Oh man! It's everywhere!!!""",
		'name' : 'Kaboom!'
	})
	
	db.stamps.save({
		'slug' : 'Surprise',
		'description' : """Well that was unexpected.""",
		'name' : 'Surprise!'
	})
	
	db.stamps.save({
		'slug' : 'SecretIngredient',
		'description' : """Shhh... don't tell anyone.""",
		'name' : 'Secret Ingredient'
	})
	
	
	db.stamps.save({
		'slug' : 'Superstar',
		'description' : '',
		'name' : 'Superstar'
	})
	'''
	
	'''
	db.badges.remove()

	db.badges.save({
		"name" : "Stoveside Hero",
		"slug" : "StovesideHero",
		"description" : "You help people survive, nay, thrive in the kitchen jungle."
	})
	
	db.badges.save({
		"name" : "Kitchen Buddy",
		"slug" : "KitchenBuddy",
		"description" : "With you around, even waiting for water to boil is fun."
	})
	
	db.badges.save({
		"name" : "Fearless Fryer",
		"slug" : "FearlessFryer",
		"description" : "Boldly going where no cook has gone before..."
	})
	

	
	db.rooms.save({
		"recipe_id" : "4f3352569685aa28d5000008",
		"users" : [ "t@tinabeans.com", "nanotone@gmail.com"]
	})
	'''
	
	'''
	meal1 = {
		"_id": ObjectId('4f3352569685aa28d5000008'),
		
		"title":"Lemon Garlic Pasta with Kale",
		
		"slug":"LemonGarlicKalePasta",
		
		"credit":"The Cilantropist",
		
		"creditURL":"http://cilantropist.blogspot.com/2011/01/easy-lemon-garlic-kale-pasta.html",
		
		"shortDescription": """A light and lemony pasta dish that's reminiscent of spring, yet inspired by winter's bounty.""",
		
		"time" : "30 min - 1 hr",
		
		"type" : "vegan",
		
		"difficulty" : "easy-peasy",
		
		"flavors" : "tart, refreshing, light",
		
		"description":"Kale is a hearty leafy green commonly found at farmer's vegetables in the late fall through early winter. Here, the nutty flavor of saut&eacute;ed kale is paired with a bright splash of lemon&mdash;a fragrant reminder that spring is not too far off!",
		
		"summary":"This pasta dish comes together quickly with just a few ingredients. The kale is saut&eacute;ed in garlic, while lemons and more garlic infuse gently into a fragrant olive oil \"sauce.\" Because of it's so easy to prepare, it's great for a low-key and healthy weeknight supper. It's also vegetarian, making it an ideal candidate for Meatless Mondays.",
		
		"ingredients":[
			{
				"amount":"1 bunch",
				"name":"kale"
			},
			{
				"amount":"1/2 box",
				"name":"fettuccine"
			},
			{
				"amount":"2",
				"name":"lemons"
			},
			{
				"amount":"3 cloves",
				"name":"fresh garlic"
			},
			{
				"amount":"1/4 cup",
				"name":"pine nuts"
			},
			{
				"name":"extra virgin olive oil"
			},
			{
				"name":"salt & pepper"
			}
		],
		
		"steps":[
			{
				"text":"<p>Gather the following ingredients:</p>",
				"type":"ingredients",
				"id":"1"
			},
			{
				"text":"<p>Mince all 3 cloves of garlic.</p>",
				"type":"prep",
				"id":"2",
				"extra":"<p>Ask your partner if they know a good trick for peeling garlic. (There are several.)</p>"
			},
			{
				"text":"<p>Wash the kale, then separate the leaves from the stems. Cut leaves into ribbons.</p>",
				"type":"prep",
				"id":"3",
				"extra":"<p>If you have kitchen scissors, here's a good chance to use them. Maybe even cut some paper doll chains!</p>"
			},
			{
				"text":"<p>Wash the lemons. Take one and slice into thin half-rounds. Take the other and zest it, then cut in half and juice it.</p>",
				"type":"prep",
				"id":"4",
				"extra":"<p>If you've never zested a lemon, your nose is in for a treat. Don't know how? See who can find out first.</p>"
			},
			{
				"text":"<p>You're done with the prep stage. Take a break and rate your partner's chopping:</p>",
				"type":"rest",
				"id":"5"
			},
			{
				"text":"""<p>Now let's crank up the heat. Add to an empty skillet:</p>
							<ul>
								<li>a tablespoon of olive oil</li>
								<li>a third of the minced garlic</li>
							</ul>
							<p>Turn on heat to medium and cook, stirring, until garlic sizzles.</p>""",
				"type":"heat",
				"id":"6",
				"extra":"<p>Starting off the garlic in cold oil is a cool trick (no pun intended). It helps \"infuse\" the oil with the garlic flavor as it heats up.</p>"
			},
			{
				"text":"<p>Now add to the skillet all the chopped kale leaves. Cook until kale is softened (5-8 minutes). Turn off the heat. Take kale out of the pan and set aside.</p>",
				"type":"heat",
				"id":"7"
			},
			{
				"text":"<p>Start cooking the pasta: bring a large pot of water to boil over high heat.</p>",
				"type":"heat",
				"id":"8"
			},
			{
				"text":"""<p>Start making the flavor-infused oil. Add to the skillet that you cooked the kale in:</p>
							<ul>
								<li>1/4 cup of olive oil</li>
								<li>the rest of the minced garlic</li>
								<li>half of the lemon slices</li>
							</ul>
							<p>Turn on the heat to medium-low. Let everything cook gently in the hot oil.</p>""",
				"type":"heat",
				"id":"9"
			},
			{
				"text":"<p>When the water starts boiling, add in half the box of pasta. Reduce heat to medium. Let the pasta cook at a rolling boil, uncovered, for about 10 minutes.",
				"type":"heat",
				"id":"10",
				"extra":"<p>What's your partner's best trick for getting long pasta to fit into the pot? (Breaking pasta doesn't count.)</p>"
			},
			{
				"text":"<p>You have a few minutes to relax while the pasta and oil are cooking, so why not sneak a taste of that kale?</p>",
				"widget":"flavors",
				"type":"rest",
				"id":"11"
			},
			{
				"text":"<p>After the pasta's been cooking for about 10 minutes, test for doneness. When the texture's to your liking, turn off the heat and drain.</p>",
				"type":"finish",
				"id":"12",
				"extra":"<p>The traditional way to cook pasta is called \"al dente,\" which is pasta that's still a tad hard in the center. It has a nice chewy resistance to the tooth. That said, how do you and your partner like your pasta?</p>"
			},
			{
				"text":"<p>The oil should be finishing up too. Turn off the heat and fish out the cooked lemons&mdash;they're bitter.</p>",
				"type":"finish",
				"id":"13"
			},
			{
				"text":"""<p>Now for the grand finale. Put everything in the pot with the pasta:</p>
							<ul>
								<li>the cooked kale</li>
								<li>the infused oil</li>
								<li>the remaining sliced lemons</li>
								<li>lemon zest</li>
								<li>lemon juice</li>
								<li>1/4 cup of pine nuts</li>
								<li>salt and pepper to taste</li>
							</ul>
							<p>Toss together and you're ready to eat!</p>""",
				"type":"finish",
				"id":"14",
				"extra":"<p>Undeniably the best way to mix any food is to put a lid on and shake. See who has the best pot-shaking dance. (Careful of hot parts!)</p>"
			},
			{
				"text":"<p>The food's ready to eat!</p>",
				"type":"eat",
				"id":"15"
			}
		]
	}
	
	db.meals.save(meal1)

	meal2 = {
		"_id": ObjectId('4f666a6b4bf254343c000001'),
	
		"slug" : "ClassicChineseSteamedFish",
		
		"title" : "Classic Chinese Steamed Fish",
		
		"credit":"Tina's mom",
		
		"creditURL":"#",
		
		"shortDescription": """A super-easy and healthy traditional standby&mdash;home cooking at its best.""",
		
		"time" : "1 hr - 2 hr",
		
		"type" : "pescatarian",
		
		"difficulty" : "easy-peasy",
		
		"flavors" : "light, savory, fragrant",
		
		"description":"""From the contributor: "Whenever I go home to visit my mom, she makes fish (there's an old Chinese believe that fish is good for your brain), so this always reminds me of home. This is so yummy, you won't believe how easy it is. My mom always uses whole fish, but fillets work just as well for those of us less culinarily gifted!"</p><p>Here we've paired it with <strong>steamed white rice</strong> and <strong>stir-fried bok choy</strong> to make a classic Chinese homecooked meal. You'll even learn traditional Chinese cooking techniques too!""",
		
		"ingredients": [
			{
				"name" : "white-fleshed fish, any kind",
				"amount": "1 lb"
			},
			{
				"name" : "scallions",
				"amount": "3 stalks"
			},
			{
				"name" : "fresh garlic",
				"amount": "6 cloves"
			},
			{
				"name" : "fresh ginger",
				"amount": '1" knob'
			},
			{
				"name" : "bok choy",
				"amount": "1 lb"
			},
			{
				"name" : "uncooked white rice",
				"amount": "1 cup"
			},
			{
				"name" : "soy sauce"
			},
			{
				"name" : "salt"
			},
			{
				"name" : "sugar"
			},
			{
				"name" : "oil, any kind"
			}
		],
		"steps": [
			{
				"id": "0",
				"type": "ingredients",
				"text": """<p>Gather the following ingredients:</p>"""
			},
			{
				"id": "1",
				"type": "prep",
				"text": """<p>Prep the ingredients:</p>
					<ul>
						<li>Wash and cut <strong>3 stalks of scallions</strong> into 2" segments.</li>
						<li>Wash and slice a <strong>1" knob of ginger</strong> into thin coins.</li>
						<li>Peel <strong>6 cloves of garlic</strong>. Slice half thinly, and mince the other half.</li>
					</ul>"""
			},
			{
				"id": "2",
				"type": "prep",
				"text": """<p>Wash and cut the bok choy into 1" chunks. Also, take out the (hopefully defrosted) fish and pat dry with paper towels or napkins.</p>"""
			},
			{
				"id": "3",
				"type": "heat",
				"text": """<p>Start the rice. Measure out:</p>
					<ul>
						<li>1 cup of rice</li>
					</ul>
					<p>Rinse the rice in cold water and drain. Then, if you have a rice cooker, use it. Otherwise add it to a pot, along with:</p>
					<ul>
						<li>1 3/4 cups water</li>
					</ul>
					<p>Turn the heat up to medium-high.</p>""",
				"extra": """<p>If you use a heavy-bottom pot, you'll greatly reduce your changes of 'burning' the bottom of the rice. But if you only have a thin pot, just use extra vigilance and you should be fine.</p>"""
			},
			{
				"id": "4",
				"type": "rest",
				"text": """<p>How did everyone's prepping go? While the rice is heating up, feel free to take a little break.</p>"""
			},
			{
				"id": "5",
				"type": "heat",
				"text": """<p>When the rice starts to boil, put a lid on and reduce heat to low. Start a timer for 15 minutes.</p>"""
			},
			{
				"id": "6",
				"type": "heat",
				"text": """<p>Heat 1 tsp of oil over high heat in a skillet, preferably nonstick. When the oil is hot, gently lay fish in the pan. Saut&eacute; about 1&ndash;2 minutes, then flip. Lightly browning the fish gives it a nicer flavor.</p>""",
				'extra' : """<p>If the fish falls apart while you're trying to flip it, never fear. It will still taste excellent!</p>"""
			},
			{
				"id": "7",
				"type": "heat",
				"text": """<p>Once the fish is nicely browned, quickly add to the pan:</p>
					<ul>
						<li>1/3 cup of water</li>
						<li>the scallions</li>
						<li>the ginger</li>
						<li>the sliced garlic only</li>
						<li>1 tbsp soy sauce</li>
						<li>1/2 teaspoon sugar</li>
					</ul>
				<p>When the liquid starts simmering, put on a lid and turn the heat down to medium-low. Steam for 7-12 minutes, depending on the thickness of the fish.</p>"""
			},
			{
				"id": "8",
				"type": "rest",
				"text": """<p>Your kitchen should start to smell pretty good soon! Why not take another break while the fish and rice are finishing up?</p>"""
			},
			{
				"id": "9",
				"type": "heat",
				"text": """<p>If it's been 15 minutes for the rice, turn off the heat. Let it sit with the lid on until you are done cooking.</p>""",
				"extra" : """<p>Resist the urge to uncover the pot. This allows the trapped steam to finish off the cooking, so you get perfectly cooked rice without burning the bottom.</p>"""
			},
			{
				"id": "10",
				"type": "heat",
				"text": """<p>When the fish is finishing up, test for done-ness by flaking it with a fork. If it's cooked through, turn off the heat and move the entire contents of the skillet to a plate.</p>
				<p>You're now ready to cook the final item: bok-choy!</p>"""
			},
			{
				"id": "11",
				"type": "heat",
				"text": """<p>Dry off the skillet and heat 1 teaspoon of oil in it, over high heat. When the oil is very hot, add:</p>
					<ul>
						<li>the rest of the minced garlic</li>
						<li>all the bok choy</li>
					</ul>
					<p>Toss around vigorously for a minute or two, then add:</p>
					<ul>
						<li>1/2 teaspoon of salt</li>
						<li>1/2 teaspoon of sugar</li>
					</ul>
					<p>Toss for another couple of minutes or so.</p>""",
				"extra" : """<p>Congrats, you've just mastered the mysterious ancient Chinese cooking technique known as stir-frying!</p>"""
			},
			{
				"id": "12",
				"type": "heat",
				"text": """<p>Add a 1/4 cup of water to the pan, bring to a boil, and cover (you know the drill by now). Let it steam for 5-7 minutes.</p>""",
				"extra" : """<p>The length of steaming depends on how crisp or tender you want your bok choy to be. That's completely a matter of personal taste.</p>"""
			},
			{
				"id": "13",
				"type": "heat",
				"text": """<p>When the bok choy is to your liking, turn off the heat. Fluff the rice. Set the table with everything you just made... and you're ready to eat!</p>"""
			},
			{
				"id": "14",
				"type": "eat",
				"text": """<p>How's it all taste?</p>"""
			}
		]
	}
	
	db.meals.save(meal2)
	
	meal3 = {
		"_id": ObjectId('4f667da14bf254378f000000'),
	
		"slug" : "AppleCheddarQuiche",
		
		"title" : "Apple Cheddar Quiche",
		
		"credit":"Closet Cooking",
		
		"creditURL":"http://www.closetcooking.com/2010/12/apple-and-cheddar-quiche.html",
		
		"shortDescription": """The flavors of apple, cheddar and rosemary combine deliciously in this savory quiche.""",
		
		"time" : "1 hr - 2 hr",
		
		"type" : "vegetarian",
		
		"difficulty" : "easy-peasy",
		
		"flavors" : "rich, savory, sweet",
		
		"description":"""Apple and cheddar: what could be better than this perfect pairing of flavors? How about adding in a dash of rosemary, a swirl of cream, and binding it all together with fresh eggs in a toasty crust? This quiche works for any meal of the day, including a light dinner. Here, we've paired it with a <strong>cranberry spinach salad</strong> in homemade <strong>balsamic vinaigrette</strong>. It reheats wonderfully for lunch the next day... that is, assuming there's any left.""",
		
		"ingredients": [
			{
				"name" : "apples",
				"amount": "2 medium"
			},
			{
				"name" : """9" pie shell""",
				"amount": "1"
			},
			{
				"name" : "eggs",
				"amount": "6"
			},
			{
				"name" : "cheddar",
				"amount": '1 lb block or shredded'
			},
			{
				"name" : "half and half",
				"amount": "1 cup"
			},
			{
				"name" : "baby spinach",
				"amount": "1 bag"
			},
			{
				"name" : "walnuts",
				"amount": "1/4 cup"
			},
			{
				"name" : "dried cranberries",
				"amount": "1/4 cup"
			},
			{
				"name" : "garlic",
				"amount" : "1 clove"
			},
			{
				"name" : "dried rosemary"
			},
			{
				"name" : "olive oil"
			},
			{
				"name" : "balsamic vinegar"
			},
			{
				"name" : "brown sugar"
			},
			{
				"name" : "salt and pepper"
			}
		],
		"steps": [
			{
				"id": "0",
				"type": "ingredients",
				"text": """<p>Gather the following ingredients:</p>"""
			},
			{
				"id": "1",
				"type": "prep",
				"text": """<p>Preheat the oven to 375 degrees F.</p>"""
			},
			{
				"id": "2",
				"type": "prep",
				"text": """<p>Prepare the quiche ingredients:</p>
					<ul>
						<li>Wash and dice the 2 apples</li>
						<li>Grate about 1 cup of cheddar, if it's in a block</li>
					</ul>"""
			},
			{
				"id": "3",
				"type": "prep",
				"text": """<p>In a large bowl, beat together:</p>
					<ul>
						<li>6 eggs</li>
						<li>1 cup of half and half</li>
						<li>1/4 teaspoon of rosemary</li>
					</ul>"""
			},
			{
				"id": "4",
				"type": "prep",
				"text": """<p>Fill the pie shell: line the bottom with the diced apples, then pour in the egg-and-cream mixture. Finally, sprinkle cheddar cheese on top.</p>""",
				"extra" : "<p>Too much filling? Save the remainder and make a mini breakfast scramble!</p>"
			},
			{
				"id": "5",
				"type": "heat",
				"text": """<p>Pop the quiche in the oven, and set a timer for 35 minutes.</p>"""
			},
			{
				"id": "6",
				"type": "rest",
				"text": """<p>Whew. Time to take a breather.</p>"""
			},
			{
				"id": "7",
				"type": "prep",
				"text": """<p>Begin making the salad:</p>
					<ul>
						<li>finely mince a single clove of garlic</li>
						<li>grate a small handful of cheddar cheese</li>
					</ul>"""
			},
			{
				"id": "8",
				"type": "prep",
				"text": """<p>Make the dressing! Pick a jar or small container with a tight-fitting lid, and put in the following:</p>
					<ul>
						<li>1/4 cup of olive oil</li>
						<li>1 1/2 tbsp of balsamic vinegar</li>
						<li>the minced garlic</li>
						<li>1 teaspoon of brown sugar</li>
						<li>a couple pinches of salt and pepper</li>
					</ul>
					<p>Put the lid on tightly and shake.</p>"""
			},
			{
				"id": "9",
				"type": "prep",
				"text": """<p>Assemble the salad! Toss the following in a bowl:</p>
					<ul>
						<li>baby spinach</li>
						<li>a handful of cranberries</li>
						<li>a handful of walnuts (see Protip)</li>
						<li>the grated cheddar</li>
					</ul>""",
				"extra" : """<p>If you have raw walnuts, toast them in the microwave! Lay them on a dish in a single layer and microwave on high for 1 minute. Be careful, they will be very hot!</p>"""
			},
			{
				"id": "10",
				"type": "rest",
				"text": """<p>You'll probably have some time left while the quiche cooks, so take another break!</p>"""
			},
			{
				"id": "11",
				"type": "heat",
				"text": """<p>When the quiche time is up, check for doneness by gently jiggling the pie pan in the oven. If the center moves, give it another 10 minutes. Otherwise, it's done!</p>""",
				"extra" : """<p>Remember to turn off the oven.</p>"""
			},
			{
				"id": "12",
				"type": "finish",
				"text": """<p>Give the quiche a few minutes to cool. Meanwhile, you can dress and toss the salad. Then cut a slice of quiche, set the table, and chow down!</p>""",
				"extra" : """<p>Best way to ensure perfectly tossed salad is to put everything in a lidded container, and&mdashyou guessed it&mdashshake. Even a bowl and upturned plate work for this purpose.</p>"""
			},
			{
				"id": "13",
				"type": "eat",
				"text": """<p>How's it all taste?</p>"""
			}
		]
	}

	db.meals.save(meal3)
	'''
	
	meal4 = {
		"_id" : ObjectId('4f8509bb9685aa744c000000'),
	
		"slug" : "GarlicCuminVinaigretteEggplant",
		
		"title" : "Grilled Eggplant with Garlic-Cumin Vinaigrette, Feta &amp; Herbs",
		
		"submittedBy" : "Beatriz",
		
		"submissionDate" : "April 10, 2011",
		
		"credit":"Fine Cooking",
		
		"creditURL":"http://www.finecooking.com/recipes/grilled-eggplant-garlic-cumin-vinaigrette-feta-herbs.aspx?nterms=112064",
		
		"shortDescription": """If you aren't a believer in eggplants, this will definitely bring you around.""",
		
		"time" : "1 hr",
		
		"servings" : "2-4 servings",
		
		"type" : "vegetarian",
		
		"difficulty" : "easy-peasy",
		
		"flavors" : "zesty, Mediterranean, fresh",
		
		"description":"""Zesty homemade vinaigrette, creamy eggplant and bright herbs served over a bed of couscous make for quite a sophisticated dinner or lunch! But it's surprisingly easy and healthy, too. Here's a presentation tip from the original site: "This dish looks especially nice served on a platter, with the feta and herbs scattered over grilled eggplant." Why not? Food that looks better, tastes better!""",
		
		"ingredients": [
			{
				"name" : "garlic",
				"amount": "1 clove"
			},
			{
				"name" : """lemon""",
				"amount": "1"
			},
			{
				"name" : "shallot",
				"amount": "1"
			},
			{
				"name" : "couscous",
				"amount": "1 cup"
			},
			{
				"name" : "globe eggplant",
				"amount": '1 large'
			},
			{
				"name" : "feta cheese",
				"amount": "1/4 cup"
			},
			{
				"name" : "fresh mint",
				"amount": "2 tbsp"
			},
			{
				"name" : "fresh cilantro",
				"amount": "2 tbsp"
			},
			{
				"name" : "salt"
			},
			{
				"name" : "cayenne pepper"
			},
			{
				"name" : "cumin"
			},
			{
				"name" : "extra virgin olive oil"
			}
			
		],
		"steps": [
			{
				"id": "0",
				"type": "ingredients",
				"text": """<p>Gather the following ingredients:</p>"""
			},
			{
				"id": "1",
				"type": "prep",
				"text": """<p>Prepare the vinaigrette ingredients:</p>
					<ul>
						<li>Squeeze the lemon.</li>
						<li>Finely dice the shallot.</li>
						<li>Mash the garlic clove.</li>
						<li>Lightly toast 1/2 teaspoon of cumin in a pan (optional).</li>
					</ul>""",
				"extra": "<p>To mash garlic, you can either pound with a mortar &amp; pestle, squeeze through a garlic press, or finely chop then mash it with a fork. A sprinkle of salt helps the garlic soften up while mashing.</p>"
			},
			{
				"id": "2",
				"type": "prep",
				"text": """<p>Combine in two separate small bowls:</p>
					<ul>
						<li>the mashed garlic</li>
						<li>1 tablespoon of lemon juice</li>
					</ul>
					<p>and</p>
					<ul>
						<li>the minced shallot</li>
						<li>1/2 tablespoon of lemon juice.</li>
					</ul>
					<p>Let sit for 10 minutes.</p>"""
			},
			{
				"id": "3",
				"type": "prep",
				"text": """<p>Meanwhile, prepare the eggplant ingredients:</p>
					<ul>
						<li>Slice the eggplant into 1/2-inch-thick slices.</li>
						<li>Chop 2 tablespoons of mint leaves.</li>
						<li>Chop 2 tablespoons of cilantro leaves.</li>
					</ul>"""
			},
			{
				"id": "4",
				"type": "prep",
				"text": """<p>Brush or rub both sides of the eggplant slices with olive oil and sprinkle on a little bit of salt.</p>"""
			},
			{
				"id" : "5",
				"type" : "heat",
				"text" : "<p>Start the couscous. Bring <strong>1 and 1/2 cup of water</strong> to boil in a medium pot. While waiting for the water, you can start cooking the eggplant..."
			},
			{
				"id": "6",
				"type": "heat",
				"text": """<p>Fire up the grill, or if you don't have a grill, heat a big non-stick skillet on high heat.</p>"""
			},
			{
				"id": "7",
				"type": "heat",
				"text": """<p>When the grill or pan is very hot, lay the slices on top. Grill/saute until slices are golden brown and feel soft when poked, about 3&ndash;4 minutes per side. If water comes to a boil during this time, see next step.</p>""",
				"extra": "<p>How to tell if the pan is hot enough? Throw a <i>tiny</i> bit of water in, and see if it immediately evaporates. Be careful if there is already oil in the pan; too much water will make the oil pop and splatter!</p>"
			},
			{
				"id": "8",
				"type": "heat",
				"text": """<p>When the water comes to a boil, add <strong>1 cup of couscous</strong>, cover tightly, and turn off the heat. Let it sit covered for 15 minutes.</p>"""
			},
			{
				"id": "9",
				"type": "finish",
				"text": """<p>Finish the vinaigrette. Whisk into the lemon-garlic mixture:</p>
					<ul>
						<li>the toasted cumin</li>
						<li>3 tablespoons of olive oil</li>
						<li>a pinch of cayenne, to taste</li>
					</ul>""",
				"extra": """<p>Tasting is everything, so treat yourself to a little sample of that vinaigrette and adjust the spices accordingly. Jot down your reaction using the notes and stamps buttons.</p>"""
			},
			{
				"id": "10",
				"type": "rest",
				"text": """Take a break while the couscous finishes steaming and the vinaigrette flavors mesh. Now's a good time to write down any thoughts, discoveries, and reactions you've had, too!"""
			},
			{
				"id": "11",
				"type": "finish",
				"text": """<p>When the couscous is done, it's ready to serve. Fluff it with a fork and put a big mound on a plate. Top with:</p>
					<ul>
						<li>a few slices of eggplant</li>
						<li>some of the shallot-lemon mixture</li>
						<li>a sprinkle of feta</li>
						<li>a sprinkle of cilantro and mint</li>
						<li>a drizzle of vinagrette</li>
					</ul>
					<p>If you're feeding more than one person, repeat this with each plate.</p>"""
			},
			{
				"id": "12",
				"type": "eat",
				"text": """<p>Time to eat! How's it taste? Write it all down here:</p>"""
			}
		]
	}

	db.meals.save(meal4)