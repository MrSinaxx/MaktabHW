import os
import shutil
from unittest import TestCase

from data_manager.file_manager import FileManager, BaseModel


class TestModel(BaseModel):
    data: str

    def __init__(self, data="Test") -> None:
        super().__init__()
        self.data = data

    def __str__(self) -> str:
        return f'TestModel #{self._id}: {self.data}'

    pass


class FileManagerTest(TestCase):
    config = {
        'ROOT_PATH': 'test_data/',
        'TRASH_PATH': 'test_data/trash/'
    }
    manager = FileManager(config)

    def setUp(self) -> None:
        root_files_path = self.config['ROOT_PATH']
        if os.path.exists(root_files_path):
            shutil.rmtree(root_files_path)

    def tearDown(self) -> None:
        root_files_path = self.config['ROOT_PATH']
        if os.path.exists(root_files_path):
            shutil.rmtree(root_files_path)

    def test1_create(self):
        test_model = TestModel("Test1")

        # Check if id is not set
        self.assertIsNone(getattr(test_model, '_id', None))

        # Creating
        self.manager.create(test_model)

        # Check if id is set
        self.assertIsNotNone(getattr(test_model, '_id', None))

    def test2_create_read(self):
        test_model = TestModel("Test2")

        # Creating
        self.manager.create(test_model)

        read_model = self.manager.read(test_model._id, test_model.__class__)
        self.assertIsNotNone(read_model)

    def test3_read_all(self):
        num_of_objs = 5
        models = []
        for i in range(num_of_objs):
            m = TestModel("Test" + str(i))
            self.manager.create(m)
            models.append(m)

        all_models = list(self.manager.read_all(TestModel))

        for m in models:
            self.assertIn(m, all_models)
    def test4_update(self):
        test_model = TestModel("Test4")

        self.manager.create(test_model)

        updated_data = "Updated Test4"
        test_model.data = updated_data

        self.manager.update(test_model)

        read_model = self.manager.read(test_model._id, test_model.__class__)
        self.assertEqual(read_model.data, updated_data)

    def test5_delete(self):
        test_model = TestModel("Test5")

        self.manager.create(test_model)

        self.manager.delete(test_model._id, test_model.__class__)

        with self.assertRaises(FileNotFoundError):
            self.manager.read(test_model._id, test_model.__class__)
            
    def test6_temporary_delete(self):
        test_model = TestModel("Test6")

        self.manager.create(test_model)

        self.manager.delete(test_model._id, test_model.__class__, temporary=True)

        with self.assertRaises(FileNotFoundError):
            self.manager.read(test_model._id, test_model.__class__)

        self.manager.restore(test_model._id, test_model.__class__)

        restored_model = self.manager.read(test_model._id, test_model.__class__)
        self.assertEqual(restored_model, test_model)