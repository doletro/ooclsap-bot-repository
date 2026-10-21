from unittest import TestCase

from app import app


class ChatTests(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/v2/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_every_message_returns_hello_world(self):
        for payload in ({"message": "Hi"}, {"message": "What is the weather?"}, {"message": ""}, {}):
            with self.subTest(payload=payload):
                response = self.client.post("/v2/chat", json=payload)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["content"], "hello world")
                self.assertEqual(response.json["type"], "execution_complete")
                self.assertTrue(response.json["conversation_id"].startswith("session-"))

    def test_existing_conversation_id_is_returned(self):
        response = self.client.post(
            "/v2/chat", json={"message": "anything", "conversation_id": "session-existing"}
        )
        self.assertEqual(response.json["conversation_id"], "session-existing")
        self.assertEqual(response.json["content"], "hello world")

    def test_missing_json_still_returns_hello_world(self):
        response = self.client.post("/v2/chat", data="anything")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["content"], "hello world")