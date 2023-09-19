#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py', 'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None, "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Setup for test methods"""
        cls.base = BaseModel()
        cls.base.name = "Kev"
        cls.base.num = 20

    @classmethod
    def tearDownClass(cls):
        """Teardown at the end of the test"""
        del cls.base

    def tearDown(self):
        """Teardown after each test method"""
        try:
            delattr(self.base, "name")
            delattr(self.base, "num")
        except AttributeError:
            pass

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)

    def test_datetime_attributes(self):
        """Test that datetime attributes are correctly created"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertIsInstance(inst1.created_at, datetime)
        self.assertIsInstance(inst1.updated_at, datetime)
        self.assertIsInstance(inst2.created_at, datetime)
        self.assertIsInstance(inst2.updated_at, datetime)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid UUID"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertIsInstance(inst1.id, str)
        self.assertIsInstance(inst2.id, str)
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertEqual(d["name"], "Holberton")
        self.assertEqual(d["my_number"], 89)
        self.assertIsInstance(d["created_at"], str)
        self.assertIsInstance(d["updated_at"], str)

    def test_str(self):
        """Test the __str__ method"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test the save method"""
        inst = BaseModel()
        old_updated_at = inst.updated_at
        inst.save()
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


if __name__ == "__main__":
    unittest.main()
