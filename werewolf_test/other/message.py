import unittest

from werewolf_server.model.message import Message


class TestMessage(unittest.TestCase):
    def test_initialization(self):
        message = Message(Message.CODE_SUCCESS, 'info', 'Success message')
        self.assertEqual(message.code, Message.CODE_SUCCESS)
        self.assertEqual(message.type, 'info')
        self.assertEqual(message.detail, 'Success message')

    def test_to_json(self):
        message = Message(Message.CODE_FAILED, 'error', 'Failure message')
        json_output = message.to_json()
        expected_json = '{"code": -1, "type": "error", "detail": "Failure message"}'
        self.assertEqual(json_output, expected_json)

    def test_from_json(self):
        json_input = '{"code": 0, "type": "info", "detail": "Success message"}'
        message = Message.from_json(json_input)
        self.assertEqual(message.code, Message.CODE_SUCCESS)
        self.assertEqual(message.type, 'info')
        self.assertEqual(message.detail, 'Success message')

    def test_str(self):
        message = Message(Message.CODE_SUCCESS, 'info', 'Success message')
        self.assertIn('Message', str(message))
        self.assertIn('code: 0', str(message))
        self.assertIn('type: info', str(message))
        self.assertIn('detail: Success message', str(message))

if __name__ == "__main__":
    unittest.main()