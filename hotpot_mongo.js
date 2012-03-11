A MEAL = {
	"_id": ObjectId("42353a3c3b..."),
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

/* 
A SNIPPET = {
	"_id": "123123",
	"type": "protip" (or "foodnote"),
	"text": "bust out...",
} */

A USERNOTE = {
	"_id": ObjectId("234234lkas897"),
	"user_id": "4123bac0132...",
	"recipe_id": "42353a3c3b...",
	"snippet_id": "123123",
	"text": "hallo"
}

A USER = {
	"_id": ObjectId("4123bac0132..."),
	"email" : "t@tinabeans.com",
	"name" : "Tina",
	"password" : "somethingencrypted",
	"location" : "New York",
	"userpic" : "4f2e0b279685aa1618000001_0.235118283529.png"
}

A ROOM = {
	"_id" : ObjectID("4123bac0132..."),
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

AN INVITATION = {
	"_id" : ObjectId("4123bac0132..."),
	"status" : "new",
	"hostId" : "4123bac0132...",
	"inviteeIds" : ["4123bac0132..."],
	"datetime" : 1330483597,
	"sendDate" : 1330483597,
	"meal" : "LemonGarlicKalePasta",
	"readableTime": "7:00 PM",
	"readableDate": "Wednesday, March 12, 2012",
	"message" : "Let's make Lemon Garlic Pasta with Kale together on Hotpot.",
	"replies" : {[
		"userId" : "4123bac0132...",
		"mainReply" : "maybe",
		"message" : "I would love to cook with you!",
		"altTimes" : "7pm Tuesday",
		"altMeals" : "Bacon!"
	]}
}












