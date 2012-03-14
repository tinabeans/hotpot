from pymongo.objectid import ObjectId

def start(db):
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

	''' db.stamps.save({
		'slug' : 'kaboom',
		'description' : """Oh man! It's everywhere!!!""",
		'name' : 'Kaboom!'
	})'''
	
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
	
	'''
	db.stamps.save({
		'slug' : 'Surprise',
		'description' : """Well that was unexpected.""",
		'name' : 'Surprise!'
	})
	'''
	
	db.stamps.save({
		'slug' : 'happyAccident',
		'description' : """Yay, that actually worked!""",
		'name' : 'Happy Accident'
	})
	
	'''
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
	
	
	
	db.recipes.remove()

	recipe = {
		"_id" : ObjectId("4f3352569685aa28d5000008"),
		"slug" : "LemonGarlicKalePasta",
		
		"description" : """Kale is a hearty leafy green commonly found at farmer's vegetables in the late fall through early winter. Here, the nutty flavor of saut&eacute;ed kale is paired with a bright splash of lemon&mdash;a fragrant reminder that spring is not too far off!""",
		
		"summary" : """This pasta dish comes together quickly with just a few ingredients. The kale is saut&eacute;ed in garlic, while lemons and more garlic infuse gently into a fragrant olive oil "sauce." Because of it's so easy to prepare, it's great for a low-key and healthy weeknight supper. It's also vegetarian, making it an ideal candidate for Meatless Mondays.""",
		
		"title" : "Lemon Garlic Pasta with Kale",
		
		"credit" : "The Cilantropist",
		
		"creditURL" : "http://cilantropist.blogspot.com/2011/01/easy-lemon-garlic-kale-pasta.html",
		
		"ingredients": [
			{
				"name" : "kale",
				"amount": "1 bunch"
			},
			{
				"name" : "fettuccine",
				"amount": "1/2 box"
			},
			{
				"name" : "lemons",
				"amount": "2"
			},
			{
				"name" : "fresh garlic",
				"amount": "3 cloves"
			},
			{
				"name" : "pine nuts",
				"amount": "1/4 cup"
			},
			{
				"name" : "extra virgin olive oil"
			},
			{
				"name" : "salt & pepper"
			}
		],
		"steps": [
			{
				"id": "1",
				"type": "ingredients",
				"text": """<p>Gather the following ingredients:</p>"""
			},
			{
				"id": "2",
				"type": "prep",
				"text": """<p>Mince all 3 cloves of garlic.</p>""",
				"extra": """<p>Ask your partner if they know a good trick for peeling garlic. (There are several.)</p>"""
			},
			{
				"id": "3",
				"type": "prep",
				"text": """<p>Wash the kale, then separate the leaves from the stems. Cut leaves into ribbons.</p>""",
				"extra": """<p>If you have kitchen scissors, here's a good chance to use them. Maybe even cut some paper doll chains!</p>"""
			},
			{
				"id": "4",
				"type": "prep",
				"text": """<p>Wash the lemons. Take one and slice into thin half-rounds. Take the other and zest it, then cut in half and juice it.</p>""",
				"extra": """<p>If you've never zested a lemon, your nose is in for a treat. Don't know how? See who can find out first.</p>"""
			},
			{
				"id": "5",
				"type": "rest",
				"text": """<p>You're done with the prep stage. Take a break and rate your partner's chopping:</p>"""
			},
			{
				"id": "6",
				"type": "heat",
				"text": """<p>Now let's crank up the heat. Add to an empty skillet:</p>
							<ul>
								<li>a tablespoon of olive oil</li>
								<li>a third of the minced garlic</li>
							</ul>
							<p>Turn on heat to medium and cook, stirring, until garlic sizzles.</p>""",
				"extra": """<p>Starting off the garlic in cold oil is a cool trick (no pun intended). It helps "infuse" the oil with the garlic flavor as it heats up.</p>"""
			},
			{
				"id": "7",
				"type": "heat",
				"text": """<p>Now add to the skillet all the chopped kale leaves. Cook until kale is softened (5-8 minutes). Turn off the heat. Take kale out of the pan and set aside.</p>"""
			},
			{
				"id": "8",
				"type": "heat",
				"text": """<p>Start cooking the pasta: bring a large pot of water to boil over high heat.</p>"""
			},
			{
				"id": "9",
				"type": "heat",
				"text": """<p>Start making the flavor-infused oil. Add to the skillet that you cooked the kale in:</p>
							<ul>
								<li>1/4 cup of olive oil</li>
								<li>the rest of the minced garlic</li>
								<li>half of the lemon slices</li>
							</ul>
							<p>Turn on the heat to medium-low. Let everything cook gently in the hot oil.</p>"""
			},
			{
				"id": "10",
				"type": "heat",
				"text": """<p>When the water starts boiling, add in half the box of pasta. Reduce heat to medium. Let the pasta cook at a rolling boil, uncovered, for about 10 minutes.""",
				"extra": """<p>What's your partner's best trick for getting long pasta to fit into the pot? (Breaking pasta doesn't count.)</p>"""
			},
			{
				"id": "11",
				"type": "rest",
				"text": """<p>You have a few minutes to relax while the pasta and oil are cooking, so why not sneak a taste of that kale?</p>""",
				"widget": """flavors"""
			},
			{
				"id": "12",
				"type": "finish",
				"text": """<p>After the pasta's been cooking for about 10 minutes, test for doneness. When the texture's to your liking, turn off the heat and drain.</p>""",
				"extra": """<p>The traditional way to cook pasta is called "al dente," which is pasta that's still a tad hard in the center. It has a nice chewy resistance to the tooth. That said, how do you and your partner like your pasta?</p>"""
			},
			{
				"id": "13",
				"type": "finish",
				"text": """<p>The oil should be finishing up too. Turn off the heat and fish out the cooked lemons&mdash;they're bitter.</p>"""
			},
			{
				"id": "14",
				"type": "finish",
				"text": """<p>Now for the grand finale. Put everything in the pot with the pasta:</p>
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
				"extra": """<p>Undeniably the best way to mix any food is to put a lid on and shake. See who has the best pot-shaking dance. (Careful of hot parts!)</p>"""
			},
			{
				"id": "15",
				"type": "eat",
				"text": """<p>The food's ready to eat!</p>"""
			}
		]
	}
	
	db.recipes.save(recipe)
'''