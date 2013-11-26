# Copyright (c) The SimpleFIN Team
# See LICENSE for details.
from unittest import TestCase
from zope.interface.verify import verifyObject
from mock import MagicMock

from banka.interface import IInfoSource
from banka.prompt import writeTo3, readFromStdin, ParentInfoSource


class ParentInfoSourceTest(TestCase):

    def fake(self):
        p = ParentInfoSource()
        p.writer = MagicMock()
        p.reader = MagicMock()
        return p

    def test_IInfoSource(self):
        verifyObject(IInfoSource, ParentInfoSource())

    def test_default(self):
        """
        By default, L{ParentInfoSource} reads from stdin and writes to channel
        3.
        """
        p = ParentInfoSource()
        self.assertEqual(p.writer, writeTo3)
        self.assertEqual(p.reader, readFromStdin)

    def test_prompt(self):
        """
        Prompt should write a prompt to the writer and get a response from
        the reader.
        """
        p = self.fake()
        p.reader.return_value = 'Returned value'
        r = p.prompt('foo')
        p.writer.assert_called_once_with({
            'action': 'prompt',
            'key': 'foo',
        })
        p.reader.assert_called_once_with()
        self.assertEqual(r, 'Returned value',
                         "Should return value from reader")

    def test_prompt_dontAskHuman(self):
        """
        C{ask_human} should be passed through.
        """
        p = self.fake()
        p.prompt('foo', ask_human=False)
        p.writer.assert_called_once_with({
            'action': 'prompt',
            'key': 'foo',
            'ask_human': False,
        })

    def test_prompt_alternatePrompt(self):
        """
        C{prompt} should be passed through.
        """
        p = self.fake()
        p.prompt('foo', prompt='bar')
        p.writer.assert_called_once_with({
            'action': 'prompt',
            'key': 'foo',
            'prompt': 'bar',
        })

    def test_save(self):
        """
        Save will write a save prompt to the writer.
        """
        p = self.fake()
        p.save('foo', 'bar')
        p.writer.assert_called_once_with({
            'action': 'save',
            'key': 'foo',
            'value': 'bar',
        })
