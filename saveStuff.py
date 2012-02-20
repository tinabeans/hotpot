from pymongo.objectid import ObjectId

def start(db):
	'''
	db.rooms.save({
		"recipe_id" : "4f3352569685aa28d5000008",
		"users" : [ "t@tinabeans.com", "nanotone@gmail.com"]
	})
	
	'''
	db.snippets.remove()
	db.recipes.remove()

	'''
	snippet1 = {
		"type": "protip",
		"text": """<p>Bust out the kitchen scissors! Fold those leaves in half and scissor off the stems. Easy.</p>"""
	}
	
	snippet2 = {
		"type": "foodnote",
		"text": """<p>This recipe doesn't use the kale stems, but they're full of possibility. How do you plan to use them later?</p>"""
	}
	
	snippet3 = {
		"type": "foodnote",
		"text": """<p>Zesting is a lot of work, but it's almost always worth it. What do you think of the smell of fresh lemon zest?</p>"""
	}
	
	snippet4 = {
		"type": "protip",
		"text": """<p>Starting off the garlic in cold oil is a cool trick (no pun intended). It helps "infuse" the oil with the garlic flavor as it heats up.</p>"""
	}
	
	snippet5 = {
		"type": "foodnote",
		"text": """<p>Go ahead, take a bite of the kale, we won't tell. How does it taste?</p>"""
	}
	
	snippet6 = {
		"type": "foodnote",
		"text": """<p>Short of breaking the pasta in half, what's your trick for getting long pasta to fit into the pot?</p>"""
	}
	
	snippet7 = {
		"type": "foodnote",
		"text": """<p>Resist the urge to stick your finger in the oil and lick it off; your finger will burn to a crisp. However take a whiff. What you think?</p>"""
	}
	
	snippet8 = {
		"type": "protip",
		"text": """<p>Die-hard pasta nerds say you should always cook noodles to "al dente," which is how the Italians traditionally do it. This just means the pasta is still a tad bit hard, and has a nice chewy resistance to the tooth. Now that you know this, go off and cook pasta the way <em>you</em> like it.</p>"""
	}
	
	for index in range(1,9):
		db.snippets.save(locals()["snippet%d" % index])
	'''

	recipe = {
		"_id" : ObjectId("4f3352569685aa28d5000008"),
		"slug": "LemonGarlicKalePasta",
		"title": "Lemon Garlic Pasta with Kale",
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
				"text": """<p>You're done with the prep stage. Take a break and...</p>
						<a href="">Award a Badge</a>
						<a href="">Add Cooking Notes</a>""",
				"widget": """badges"""
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