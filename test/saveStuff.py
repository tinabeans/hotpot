def start(db):

	db.rooms.save({
		"recipe_id" : "4f3352569685aa28d5000008",
		"users" : [ "t@tinabeans.com", "nanotone@gmail.com"]
	})
	
	'''
	db.snippets.remove()
	db.recipes.remove()

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
	
	recipe = {
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
				"type": "prep",
				"text": """<p>Mince the 3 cloves of garlic.</p>"""
			},
			{
				"type": "prep",
				"text": """<p>Wash the kale, then separate the leaves from the stems. Cut leaves into ribbons.</p>""",
				"snippets": [ snippet1['_id'], snippet2['_id'] ]
			},
			{
				"type": "prep",
				"text": """<p>Wash the lemons. Slice one into thin half-rounds. Zest and juice the other one.</p>""",
				"snippets": [ snippet3['_id'] ]
			},
			{
				"type": "heat",
				"text": """<p>Add to the skillet:
							<ul>
								<li>about a tablespoon of olive oil</li>
								<li>about a third of the minced garlic</li>
							</ul>
							<p>Turn on heat to medium and cook, stirring, until garlic sizzles.</p>""",
				"snippets": [ snippet4['_id'] ]
			},
			{
				"type": "heat",
				"text": """<p>Add the kale leaves to the skillet. Cook until kale is softened (5-8 minutes). Turn off the heat. Take kale out of the pan and set aside.</p>""",
				"snippets": [ snippet5['_id'] ]
			},
			{
				"type": "heat",
				"text": """<p>Start cooking the pasta: bring a large pot of water to boil over high heat. While it's heating up, you can start the next step.</p>"""
			},
			{
				"type": "heat",
				"text": """<p>Start making the flavor-infused oil: Add to the empty skillet:</p>
							<ul>
								<li>1/4 cup of olive oil</li>
								<li>the rest of the garlic</li>
								<li>half of the sliced lemons</li>
							</ul>
							<p>Turn on the heat to medium-low. Let everything cook in the hot oil for about 10 minutes.</p>"""
			},
			{
				"type": "heat",
				"text": """<p>When the water starts boiling, add in half the box of pasta. Reduce heat to medium. Let the pasta cook for about 10-14 minutes.</p>""",
				"snippets": [ snippet6['_id'] ]
			},
			{
				"type": "heat",
				"text": """<p>When the oil has finished infusing, turn off the heat and remove the lemons.</p>""",
				"snippets": [ snippet7['_id'] ]
			},
			{
				"type": "finish",
				"text": """<p>The pasta should be finishing up too. Test for done-ness. Turn off the heat when the pasta texture is to your liking.</p>""",
				"snippets": [ snippet8['_id'] ]
			},
			{
				"type": "finish",
				"text": """<p>Drain the pasta. Put everything in the pot with the pasta:</p>
							<ul>
								<li>the cooked kale</li>
								<li>the infused oil</li>
								<li>the remaining sliced lemons</li>
								<li>lemon zest</li>
								<li>lemon juice</li>
								<li>1/4 cup of pine nuts</li>
								<li>salt and pepper to taste</li>
							</ul>
							<p>Toss together and you're ready to eat!</p>"""
			}
		]
	}
	
	db.recipes.save(recipe)
	'''