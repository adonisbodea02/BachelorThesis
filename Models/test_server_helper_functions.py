import unittest
from server import get_weekday_n_days_ago, construct_model_eur_gbp, construct_model_gbp_usd, construct_model_eur_usd, \
    get_data
from datetime import datetime
from tensorflow import keras


class TestGetWeekdayNDaysAgo(unittest.TestCase):

    # test for a Monday
    def test1(self):
        self.assertEqual(datetime.strptime("2020-05-04", '%Y-%m-%d'),
                         get_weekday_n_days_ago(datetime.strptime("2020-05-25", '%Y-%m-%d'), 15))

    # test for a Tuesday
    def test2(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-26", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-05", '%Y-%m-%d'))

    # test for a Wednesday
    def test3(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-27", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-06", '%Y-%m-%d'))

    # test for a Thursday
    def test4(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-28", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-07", '%Y-%m-%d'))

    # test for a Friday
    def test5(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-29", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-08", '%Y-%m-%d'))

    # test for a Saturday
    def test6(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-23", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-04", '%Y-%m-%d'))

    # test for a Sunday
    def test7(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-24", '%Y-%m-%d'), 15), datetime.
                         strptime("2020-05-04", '%Y-%m-%d'))

    # test for 1 days back
    def test8(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-26", '%Y-%m-%d'), 1), datetime.
                         strptime("2020-05-25", '%Y-%m-%d'))

    # test for 29 days back
    def test9(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-04-27", '%Y-%m-%d'), 20), datetime.
                         strptime("2020-03-30", '%Y-%m-%d'))

    # test for 1st of May
    def test10(self):
        self.assertEqual(get_weekday_n_days_ago(datetime.strptime("2020-05-08", '%Y-%m-%d'), 5), datetime.
                         strptime("2020-04-30", '%Y-%m-%d'))


class TestGetData(unittest.TestCase):

    # test that the call goes through
    def test1(self):
        self.assertEqual(15, len(get_data(datetime.strptime("2020-05-29", '%Y-%m-%d').date(), 15, "EUR", "GBP")))

    # test for n = 1
    def test2(self):
        self.assertEqual(1, len(get_data(datetime.strptime("2020-05-29", '%Y-%m-%d').date(), 1, "EUR", "GBP")))

    # test for n = 20
    def test3(self):
        self.assertEqual(20, len(get_data(datetime.strptime("2020-05-29", '%Y-%m-%d').date(), 20, "EUR", "GBP")))


class TestConstructEURGBPModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model_eur_gbp = construct_model_eur_gbp()

    @classmethod
    def tearDownClass(cls):
        keras.backend.clear_session()

    # test the number of layers
    def test1(self):
        self.assertEqual(len(self.model_eur_gbp.layers), 2)

    # test the layers' types
    def test2(self):
        self.assertEqual(self.model_eur_gbp.layers[0].name, 'lstm')
        self.assertEqual(self.model_eur_gbp.layers[1].name, 'dense')

    # test the layers' input shapes
    def test3(self):
        self.assertEqual(self.model_eur_gbp.layers[0].input_shape[1], 15)
        self.assertEqual(self.model_eur_gbp.layers[1].input_shape[1], 100)

    # test the layers' output shapes
    def test4(self):
        self.assertEqual(self.model_eur_gbp.layers[0].output_shape[1], 100)
        self.assertEqual(self.model_eur_gbp.layers[1].output_shape[1], 1)

    # test the layers' activation functions
    def test5(self):
        self.assertEqual(self.model_eur_gbp.layers[0].get_config()['activation'], 'relu')
        self.assertEqual(self.model_eur_gbp.layers[1].get_config()['activation'], 'linear')


class TestConstructEURUSDModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model_eur_usd = construct_model_eur_usd()

    @classmethod
    def tearDownClass(cls):
        keras.backend.clear_session()

    # test the number of layers
    def test1(self):
        self.assertEqual(len(self.model_eur_usd.layers), 2)

    # test the layers' types
    def test2(self):
        self.assertEqual(self.model_eur_usd.layers[0].name, 'lstm')
        self.assertEqual(self.model_eur_usd.layers[1].name, 'dense')

    # test the layers' input shapes
    def test3(self):
        self.assertEqual(self.model_eur_usd.layers[0].input_shape[1], 15)
        self.assertEqual(self.model_eur_usd.layers[1].input_shape[1], 100)

    # test the layers' output shapes
    def test4(self):
        self.assertEqual(self.model_eur_usd.layers[0].output_shape[1], 100)
        self.assertEqual(self.model_eur_usd.layers[1].output_shape[1], 1)

    # test the layers' activation functions
    def test5(self):
        self.assertEqual(self.model_eur_usd.layers[0].get_config()['activation'], 'relu')
        self.assertEqual(self.model_eur_usd.layers[1].get_config()['activation'], 'linear')


class TestConstructGBPUSDModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model_gbp_usd = construct_model_gbp_usd()

    @classmethod
    def tearDownClass(cls):
        keras.backend.clear_session()

    # test the number of layers
    def test1(self):
        self.assertEqual(len(self.model_gbp_usd.layers), 2)

    # test the layers' types
    def test2(self):
        self.assertEqual(self.model_gbp_usd.layers[0].name, 'lstm')
        self.assertEqual(self.model_gbp_usd.layers[1].name, 'dense')

    # test the layers' input shapes
    def test3(self):
        self.assertEqual(self.model_gbp_usd.layers[0].input_shape[1], 15)
        self.assertEqual(self.model_gbp_usd.layers[1].input_shape[1], 100)

    # test the layers' output shapes
    def test4(self):
        self.assertEqual(self.model_gbp_usd.layers[0].output_shape[1], 100)
        self.assertEqual(self.model_gbp_usd.layers[1].output_shape[1], 1)

    # test the layers' activation functions
    def test5(self):
        self.assertEqual(self.model_gbp_usd.layers[0].get_config()['activation'], 'tanh')
        self.assertEqual(self.model_gbp_usd.layers[1].get_config()['activation'], 'linear')

