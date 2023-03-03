from typing import Dict, Type, Final


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Возвращает информацию о тренировке и её параметрах"""

        msg: str = (f'Тип тренировки: {self.training_type}; '
                    f'Длительность: {self.duration:.3f} ч.; '
                    f'Дистанция: {self.distance:.3f} км; '
                    f'Ср. скорость: {self.speed:.3f} км/ч; '
                    f'Потрачено ккал: {self.calories:.3f}.')

        return msg


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM: Final[float] = 1000
    MIN_IN_HOUR: Final[float] = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dstnc = self.action * self.LEN_STEP / self.M_IN_KM
        return dstnc

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_spd = self.get_distance() / self.duration
        return avg_spd

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: Final[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: Final[float] = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий"""

        calo = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.MIN_IN_HOUR * self.duration))
        return calo


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: Final[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: Final[float] = 0.029
    KM_IN_MS: Final[float] = 0.278
    CM_IN_M: Final[int] = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий"""

        calo = ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed() * self.KM_IN_MS)**2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_HOUR))
        return calo


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_SHIFT: Final[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: Final[int] = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        """Получить количество потраченных калорий"""

        swim_calo = ((self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                     * self.CALORIES_WEIGHT_MULTIPLIER
                     * self.weight
                     * self.duration)
        return swim_calo

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""

        swim_spd = (self.length_pool * self.count_pool / self.M_IN_KM
                    / self.duration)
        return swim_spd


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type in training_dict:
        return training_dict[workout_type](*data)
    else:
        raise KeyError('Выбрана неподдержимаемая тренировка')


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()

    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
