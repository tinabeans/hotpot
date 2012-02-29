A RECIPE = {
	"_id": "42353a3c3b...",
	"title": "kale and..",
	"slug" : "LemonGarlicKalePasta",
	"ingredients": [
		{
			"name" : "kale",
			"amount": "1 bunch"
		],
		...
	],
	"steps": [
		{
			"type": "finish",
			"text": "wash the kale..."
		},
		...
	],
}

A SNIPPET = {
	"_id": "123123",
	"type": "protip" (or "foodnote"),
	"text": "bust out...",
}

A USERNOTE = {
	"_id": "234234lkas897",
	"user_id": "...@...",
	"recipe_id": "42353a3c3b...",
	"snippet_id": "123123",
	"text": "hallo"
}

A USER = {
	"_id": "234234lkas897",
	"email" : "t@tinabeans.com",
	"name" : "Tina",
	"password" : "somethingencrypted"
}

A ROOM = {
	"_id" : "4123bac0132...",
	"recipe_id" : "42353a3c3b...",
	"users" : [ "adfadfasdf", "asdfasdfasdf", ...]
}

A BADGE GIVEN = {
	"giverId": "e@mail.com",
	"receiverId": "t@tinabeans.com",
	"badgeSlug": "42353a3c3b…",
	"roomId": "4123bac0132…",
	"stepId": "9"
}

AN INVITE = {
	"_id" : "4123bac0132...",
	"status" : "waiting for reply",
	"from" : "t@tinabeans.com",
	"to" : "nanotone@gmail.com",
	"datetime" : 1330483597,
	"recipe" : "LemonGarlicKalePasta",
	"friendName" : "Yang",
	"message" : "Let's make Lemon Garlic Pasta with Kale together on Hotpot."
}












