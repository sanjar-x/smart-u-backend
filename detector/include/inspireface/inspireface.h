//
// Создано tunm 2023/10/3.
//

#ifndef HYPERFACEREPO_INSPIREFACE_H
#define HYPERFACEREPO_INSPIREFACE_H

#include <stdint.h>
#include "intypedef.h"
#include "herror.h"

#if defined(_WIN32)
#ifdef ISF_BUILD_SHARED_LIBS
#define HYPER_CAPI_EXPORT __declspec(dllexport)
#else
#define HYPER_CAPI_EXPORT
#endif
#else
#define HYPER_CAPI_EXPORT __attribute__((visibility("default")))
#endif // _WIN32

#ifdef __cplusplus
extern "C"
{
#endif

#define HF_ENABLE_NONE 0x00000000             ///< Флаг для отключения всех функций.
#define HF_ENABLE_FACE_RECOGNITION 0x00000002 ///< Флаг для включения функции распознавания лиц.
#define HF_ENABLE_LIVENESS 0x00000004         ///< Флаг для включения функции определения жизненности по RGB.
#define HF_ENABLE_IR_LIVENESS 0x00000008      ///< Флаг для включения функции определения жизненности по ИК (инфракрасному излучению).
#define HF_ENABLE_MASK_DETECT 0x00000010      ///< Флаг для включения функции обнаружения масок.
#define HF_ENABLE_FACE_ATTRIBUTE 0x00000020   ///< Флаг для включения функции предсказания атрибутов лица.
#define HF_ENABLE_PLACEHOLDER_ 0x00000040     ///< -
#define HF_ENABLE_QUALITY 0x00000080          ///< Флаг для включения функции оценки качества лица.
#define HF_ENABLE_INTERACTION 0x00000100      ///< Флаг для включения функции взаимодействия.

    /**
     * Формат потока камеры.
     * Содержит несколько общих форматов потоков камер, доступных на рынке.
     */
    typedef enum HFImageFormat
    {
        HF_STREAM_RGB = 0,      ///< Изображение в формате RGB.
        HF_STREAM_BGR = 1,      ///< Изображение в формате BGR (по умолчанию в OpenCV Mat).
        HF_STREAM_RGBA = 2,     ///< Изображение в формате RGB с альфа-каналом.
        HF_STREAM_BGRA = 3,     ///< Изображение в формате BGR с альфа-каналом.
        HF_STREAM_YUV_NV12 = 4, ///< Изображение в формате YUV NV12.
        HF_STREAM_YUV_NV21 = 5, ///< Изображение в формате YUV NV21.
    } HFImageFormat;

    /**
     * Режим поворота изображения с камеры.
     * Для учета поворота определенных устройств предоставляются четыре режима поворота изображения.
     */
    typedef enum HFRotation
    {
        HF_CAMERA_ROTATION_0 = 0,   ///< Поворот на 0 градусов.
        HF_CAMERA_ROTATION_90 = 1,  ///< Поворот на 90 градусов.
        HF_CAMERA_ROTATION_180 = 2, ///< Поворот на 180 градусов.
        HF_CAMERA_ROTATION_270 = 3, ///< Поворот на 270 градусов.
    } HFRotation;

    /**
     * Структура данных буфера изображения.
     * Определяет структуру для потока данных изображения.
     */
    typedef struct HFImageData
    {
        uint8_t *data;        ///< Указатель на поток данных изображения.
        HInt32 width;         ///< Ширина изображения.
        HInt32 height;        ///< Высота изображения.
        HFImageFormat format; ///< Формат изображения, указывающий формат потока данных для анализа.
        HFRotation rotation;  ///< Угол поворота изображения.
    } HFImageData, *PHFImageData;

    /**
     * @brief Создает объект экземпляра потока данных буфера.
     *
     * Эта функция используется для создания экземпляра потока данных буфера с заданными данными изображения.
     *
     * @param data Указатель на структуру данных буфера изображения.
     * @param handle Указатель на дескриптор потока, который будет возвращен.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFCreateImageStream(PHFImageData data, HFImageStream *handle);

    /**
     * @brief Освободить инстанцированный объект DataBuffer.
     *
     * Эта функция используется для освобождения объекта DataBuffer, который был ранее инстанцирован.
     *
     * @param streamHandle Указатель на дескриптор DataBuffer, представляющий компонент потока камеры.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFReleaseImageStream(HFImageStream streamHandle);

    /************************************************************************
     * Функция ресурсов
     ************************************************************************/

    /**
     * @brief Запуск InspireFace SDK
     * Запустите InspireFace SDK на этапе инициализации вашей программы, так как он глобальный и
     * предназначен для использования только один раз. Это является предпосылкой для других интерфейсов функций, поэтому важно убедиться, что он инициализирован перед вызовом любых других API.
     * @param resourcePath Инициализирует путь к файлу ресурсов, который необходимо загрузить
     * @return HResult, указывающий на успех или неудачу операции.
     * */
    HYPER_CAPI_EXPORT extern HResult HFLaunchInspireFace(HPath resourcePath);

    /**
     * @brief Завершение работы InspireFace SDK
     * Завершите работу InspireFace SDK, освободив все выделенные ресурсы.
     * Это следует вызвать в конце вашей программы для обеспечения правильной очистки.
     * @return HResult, указывающий на успех или неудачу операции.
     * */
    HYPER_CAPI_EXPORT extern HResult HFTerminateInspireFace();

    /************************************************************************
     * FaceContext
     ************************************************************************/

    /**
     * @brief Структура для пользовательских параметров в контексте распознавания лиц.
     *
     * Эта структура содержит различные флаги для включения или отключения конкретных функций
     * в контексте распознавания лиц, таких как распознавание лиц, определение жизненности,
     * обнаружение масок, предсказание возраста и пола и т. д.
     */
    typedef struct HFSessionCustomParameter
    {
        HInt32 enable_recognition;          ///< Включить функцию распознавания лиц.
        HInt32 enable_liveness;             ///< Включить функцию определения жизненности по RGB.
        HInt32 enable_ir_liveness;          ///< Включить функцию определения жизненности по ИК.
        HInt32 enable_mask_detect;          ///< Включить функцию обнаружения масок.
        HInt32 enable_face_quality;         ///< Включить функцию оценки качества лица.
        HInt32 enable_face_attribute;       ///< Включить функцию предсказания атрибутов лица.
        HInt32 enable_interaction_liveness; ///< Включить взаимодействие для функции определения жизненности.
    } HFSessionCustomParameter, *PHFSessionCustomParameter;

    /**
     * @brief Перечисление режимов обнаружения лиц.
     */
    typedef enum HFDetectMode
    {
        HF_DETECT_MODE_ALWAYS_DETECT,      ///< Режим обнаружения изображений, всегда обнаруживать, применимо к изображениям.
        HF_DETECT_MODE_LIGHT_TRACK,        ///< Режим обнаружения видео, отслеживание лица, применимо к видеопотокам, передняя камера.
        HF_DETECT_MODE_TRACK_BY_DETECTION, ///< Режим обнаружения видео, отслеживание лица, применимо к высокому разрешению, мониторинг, захват
                                           ///< (Требуется включение конкретной опции на этапе компиляции для его использования).
    } HFDetectMode;

    /**
     * @brief Создать сеанс из файла ресурсов.
     *
     * @param parameter Пользовательские параметры для сеанса.
     * @param detectMode Режим обнаружения, который будет использоваться.
     * @param maxDetectFaceNum Максимальное количество лиц для обнаружения.
     * @param detectPixelLevel Измените уровень разрешения ввода детектора, чем больше, тем лучше,
     *          необходимо вводить кратное 160, например, 160, 320, 640, значение по умолчанию -1 - это 320.
     * @param trackByDetectModeFPS Если вы используете режим отслеживания MODE_TRACK_BY_DETECTION,
     *          это значение используется для установки fps частоты кадров вашего текущего входящего видеопотока,
     * по умолчанию -1 при 30fps.
     * @param handle Указатель на дескриптор контекста, который будет возвращен.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFCreateInspireFaceSession(
        HFSessionCustomParameter parameter, HFDetectMode detectMode, HInt32 maxDetectFaceNum,
        HInt32 detectPixelLevel, HInt32 trackByDetectModeFPS, HFSession *handle);

    /**
     * @brief Создать сеанс из файла ресурсов с дополнительными опциями.
     *
     * @param customOption Пользовательская опция для дополнительной настройки.
     * @param detectMode Режим обнаружения, который будет использоваться.
     * @param maxDetectFaceNum Максимальное количество лиц для обнаружения.
     *

 @param detectPixelLevel Измените уровень разрешения ввода детектора, чем больше, тем лучше,
     *          необходимо вводить кратное 160, например, 160, 320, 640, значение по умолчанию -1 - это 320.
     * @param trackByDetectModeFPS Если вы используете режим отслеживания MODE_TRACK_BY_DETECTION,
     *          это значение используется для установки fps частоты кадров вашего текущего входящего видеопотока,
     * по умолчанию -1 при 30fps.
     * @param handle Указатель на дескриптор контекста, который будет возвращен.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFCreateInspireFaceSessionOptional(
        HOption customOption, HFDetectMode detectMode, HInt32 maxDetectFaceNum, HInt32 detectPixelLevel,
        HInt32 trackByDetectModeFPS, HFSession *handle);

    /**
     * @brief Освободить сеанс.
     *
     * @param handle Дескриптор сеанса, который необходимо освободить.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFReleaseInspireFaceSession(HFSession handle);

    /**
     * @brief Структура, представляющая базовый токен для данных лица.
     *
     * Эта структура содержит размер и указатель на данные базового токена, связанного с данными лица.
     */
    typedef struct HFFaceBasicToken
    {
        HInt32 size; ///< Размер токена.
        HPVoid data; ///< Указатель на данные токена.
    } HFFaceBasicToken, *PHFFaceBasicToken;

    /**
     * @brief Структура для углов Эйлера лица.
     *
     * Эта структура представляет углы Эйлера (ролл, рыскание, тангаж) для ориентации лица.
     */
    typedef struct HFFaceEulerAngle
    {
        HFloat *roll;  ///< Угол крена лица.
        HFloat *yaw;   ///< Угол рыскания лица.
        HFloat *pitch; ///< Угол тангажа лица.
    } HFFaceEulerAngle;

    /**
     * @brief Структура для хранения данных о нескольких обнаруженных лицах.
     *
     * Эта структура хранит данные, связанные с несколькими обнаруженными лицами, включая количество лиц,
     * их ограничивающие прямоугольники, идентификаторы треков, углы и токены.
     */
    typedef struct HFMultipleFaceData
    {
        HInt32 detectedNum;       ///< Количество обнаруженных лиц.
        HFaceRect *rects;         ///< Массив ограничивающих прямоугольников для каждого лица.
        HInt32 *trackIds;         ///< Массив идентификаторов треков для каждого лица.
        HFFaceEulerAngle angles;  ///< Углы Эйлера для каждого лица.
        PHFFaceBasicToken tokens; ///< Токены, связанные с каждым лицом.
    } HFMultipleFaceData, *PHFMultipleFaceData;

    /**
     * @brief Установить размер предварительного просмотра трека в сеансе, он работает с алгоритмами обнаружения и отслеживания лиц. Размер предварительного просмотра по умолчанию составляет 192 (пикс).
     *
     * @param session Дескриптор сеанса.
     * @param previewSize Размер предварительного просмотра для отслеживания.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFSessionSetTrackPreviewSize(HFSession session,
                                                                  HInt32 previewSize);

    /**
     * @brief Установить минимальное количество пикселей лица, которое может захватить детектор лица, и люди ниже этого числа будут отфильтрованы.
     *
     * @param session Дескриптор сеанса.
     * @param minSize Минимальное значение пикселей, значение по умолчанию - 24.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFSessionSetFilterMinimumFacePixelSize(HFSession session,
                                                                            HInt32 minSize);

    /**
     * @brief Установить порог обнаружения лица в сеансе.
     *
     * @param session Дескриптор сеанса.
     * @param detectMode Режим обнаружения для отслеживания.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFSessionSetFaceDetectThreshold(HFSession session,
                                                                     HFloat threshold);

    /**
     * @brief Запустить отслеживание лица в сеансе.
     *
     * @param session Дескриптор сеанса.
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param results Указатель на структуру, в которой будут храниться результаты.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFExecuteFaceTrack(HFSession session, HFImageStream streamHandle,
                                                        PHFMultipleFaceData results);

    /**
     * @brief Копирует данные из HF_FaceBasicToken в указанный буфер.
     *
     * Эта функция копирует данные, на которые указывает поле data HF_FaceBasicToken,
     * в предоставленный пользователем буфер. Заявитель несет ответственность за то, чтобы буфер
     * был достаточно большим для хранения копируемых данных.
     *
     * @param token HF_FaceBasicToken, содержащий данные для копирования.
     * @param buffer Буфер, в который будут скопированы данные.
     * @param bufferSize Размер буфера, предоставленного заявителем. Должен быть достаточно большим,
     *        чтобы содержать данные, на которые указывает поле data токена.
     * @return HResult, указывающий на успех или неудачу операции. Возвращает HSUCCEED
     *         если операция прошла успешно или код ошибки, если буфер был слишком мал
     *         или возникла любая другая ошибка.
     */
    HYPER_CAPI_EXPORT extern HResult HFCopyFaceBasicToken(HFFaceBasicToken token, HPBuffer buffer,
                                                          HInt32 bufferSize);

    /**
     * @brief Получает размер данных, содержащихся в HF_FaceBasicToken.
     *
     * Эта функция используется для запроса размера данных, которые содержит HF_FaceBasicToken.
     * Это полезно для выделения буфера соответствующего размера
     * перед копированием данных из HF_FaceBasicToken.
     *
     * @param bufferSize Указатель на целое число, в котором будет храниться размер данных.
     *        После успешного выполнения в нем будет содержаться размер данных в байтах.
     * @return HResult, указывающий на успех или неудачу операции. Возвращает HSUCCEED
     *         если операция прошла успешно или код ошибки, если не удалось.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceBasicTokenSize(HPInt32 bufferSize);

    /**
     * @brief Получить количество плотных лицевых маркеров.
     * @param num Количество плотных лицевых маркеров
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetNumOfFaceDenseLandmark(HPInt32 num);

    /**
     * @brief Когда вы передаете действительный лицевой токен, вы можете получить набор плотных лицевых маркеров.
     *          Память для плотных маркеров должна быть выделена вами.
     * @param singleFace Базовый токен, представляющий одно лицо.
     * @param landmarks Предварительно выделенный адрес памяти массива для 2D координат с плавающей запятой.
     * @param num Количество точек маркера
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceDenseLandmarkFromFaceToken(HFFaceBasicToken singleFace,
                                                                         HPoint2f *landmarks,
                                                                         HInt32 num);

    /************************************************************************
     * Распознавание лиц
     ************************************************************************/

    /**
     * @brief Структура, представляющая лицевой признак.
     *
     * Эта структура содержит данные, связанные с лицевым признаком, включая размер и сами данные признака.
     */
    typedef struct HFFaceFeature
    {
        HInt32 size;  ///< Размер данных признака.
        HPFloat data; ///< Указатель на данные признака.
    } HFFaceFeature, *PHFFaceFeature;

    /**
     * @brief Извлечь лицевой признак из заданного лица.
     *
     * @param session Дескриптор сеанса.
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param singleFace Базовый токен, представляющий одно лицо.
     * @param feature Указатель на извлеченный лицевой признак.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFaceFeatureExtract(
        HFSession session,
        HFImageStream streamHandle,
        HFFaceBasicToken singleFace,
        PHFFaceFeature feature);

    /**
     * @brief Извлечь лицевой признак из заданного лица и скопировать его в предоставленный буфер признака.
     *
     * @param session Дескриптор сеанса.
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param singleFace Базовый токен, представляющий одно лицо.
     * @param feature Указатель на буфер, в который будет скопирован извлеченный признак.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFaceFeatureExtractCpy(HFSession session,
                                                             HFImageStream streamHandle,
                                                             HFFaceBasicToken singleFace,
                                                             HPFloat feature);

    /************************************************************************
     * Центр признаков
     ************************************************************************/

    /**
     * @brief Выбрать режим поиска в процессе поиска по лицам,
     * и разные режимы будут влиять на эффективность выполнения и результаты
     * */
    typedef enum HFSearchMode
    {
        HF_SEARCH_MODE_EAGER = 0,  // Режим Eager: Останавливается, когда вектор достигает порога.
        HF_SEARCH_MODE_EXHAUSTIVE, // Режим Exhaustive: Ищет до нахождения наилучшего совпадения.
    } HFSearchMode;

    /**
     * @brief Структура для конфигурации базы данных.
     *
     * Эта структура содержит настройки конфигурации для использования базы данных в контексте распознавания лиц.
     */
    typedef struct HFFeatureHubConfiguration
    {
        HInt32 featureBlockNum;   ///< Порядок величины базы данных лицевых признаков составляет N * 512, по умолчанию рекомендуется 20
        HInt32 enablePersistence; ///< Флаг для включения или отключения использования базы данных.
        HString dbPath;           ///< Путь к файлу базы данных.
        float searchThreshold;    ///< Порог для поиска лиц
        HFSearchMode searchMode;  ///< Режим поиска лиц
    } HFFeatureHubConfiguration;

    /**
     * @brief Легковесное управление вектором признаков лица.
     * @details FeatureHub - это встроенная глобальная легковесная функция управления векторами признаков лиц, предоставляемая в InspireFace-SDK. Она поддерживает базовый поиск, удаление и модификацию признаков лиц,
     * и предлагает два опциональных режима хранения данных: модель в памяти и модель постоянного хранения. Если у вас есть простые потребности в хранении, вы можете включить ее.
     *
     * @param configuration Подробности конфигурации FeatureHub.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubDataEnable(HFFeatureHubConfiguration configuration);

    /**
     * @brief Отключить глобальную функцию FeatureHub, и вы можете включить ее снова при необходимости.
     * @return HResult, указывающий на успех или неудачу операции.
     * */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubDataDisable();

    /**
     * @brief Структура, представляющая идентичность лицевого признака.
     *
     * Эта структура связывает пользовательский идентификатор и тег с конкретным лицевым признаком.
     */
    typedef struct HFFaceFeatureIdentity
    {
        HInt32 customId;        ///< Пользовательский идентификатор для лицевого признака.
        HString tag;            ///< Тег, связанный с лицевым признаком.
        PHFFaceFeature feature; ///< Указатель на лицевой признак.
    } HFFaceFeatureIdentity, *PHFFaceFeatureIdentity;

    /**
     * Структура поиска для режима top-k
     * */
    typedef struct HFSearchTopKResults
    {
        HInt32 size;        ///< Количество найденных лиц
        HPFloat confidence; ///< Уверенность в поиске (она уже была отфильтрована один раз по порогу)
        HPInt32 customIds;  ///< Настроенные идентификаторы лиц
    } HFSearchTopKResults, *PHFSearchTopKResults;

    /**
     * @brief Установить порог поиска по лицам.
     *
     * Эта функция устанавливает порог для распознавания лиц, который определяет чувствительность
     * процесса распознавания. Более низкий порог может привести к большему количеству совпадений, но с меньшей уверенностью.
     *
     * @param threshold Значение порога для установки распознавания лиц (по умолчанию 0.48, подходит для сценариев контроля доступа).
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubFaceSearchThresholdSetting(float threshold);

    /**
     * @brief Выполнить сравнение один-к-одному двух лицевых признаков.
     *
     * @param session Дескриптор сеанса.
     * @param feature1 Первый лицевой признак для сравнения.
     * @param feature2 Второй лицевой признак для сравнения.
     * @param result Указатель на значение с плавающей запятой, в котором будет храниться результат сравнения.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFaceComparison(HFFaceFeature feature1, HFFaceFeature feature2,
                                                      HPFloat result);

    /**
     * @brief Получить длину лицевого признака.
     *
     * @param num Указатель на целое число, в котором будет храниться длина признака.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFeatureLength(HPInt32 num);

    /**
     * @brief Вставить идентичность лицевого признака в группу признаков.
     *
     * @param featureIdentity Лицевая идентичность признака для вставки.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubInsertFeature(HFFaceFeatureIdentity featureIdentity);

    /**
     * @brief Поиск наиболее похожего лицевого признака в группе признаков.
     *
     * @param searchFeature Лицевой признак для поиска.
     * @param confidence Указатель на значение с плавающей запятой, в котором будет храниться уровень уверенности совпадения.
     * @param mostSimilar Указатель на наиболее похожую найденную идентичность лицевого признака.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubFaceSearch(HFFaceFeature searchFeature,
                                                            HPFloat confidence,
                                                            PHFFaceFeatureIdentity mostSimilar);

    /**
     * @brief Поиск наиболее похожих k лицевых признаков в группе признаков
     *
     * @param searchFeature Лицевой признак для поиска.
     * @param confidence topK Максимальное количество поисков
     * @param PHFSearchTopKResults Результат поиска
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubFaceSearchTopK(HFFaceFeature searchFeature,
                                                                HInt32 topK,
                                                                PHFSearchTopKResults results);

    /**
     * @brief Удалить лицевой признак из группы признаков на основе пользовательского идентификатора.
     *
     * @param customId Пользовательский идентификатор признака, который нужно удалить.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubFaceRemove(HInt32 customId);

    /**
     * @brief Обновить идентичность лицевого признака в группе признаков.
     *
     * @param featureIdentity Лицевая идентичность признака для обновления.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubFaceUpdate(HFFaceFeatureIdentity featureIdentity);

    /**
     * @brief Получить идентичность лицевого признака из группы признаков на основе пользовательского идентификатора.
     *
     * @param customId Пользовательский идентификатор признака.
     * @param identity Указатель на идентичность лицевого признака для извлечения.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubGetFaceIdentity(HInt32 customId,
                                                                 PHFFaceFeatureIdentity identity);

    /**
     * @brief Получить количество лицевых признаков в группе признаков.
     *
     * @param count Указатель на целое число, в котором будет храниться количество признаков.
     * @return HResult, указыва

ющий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubGetFaceCount(HInt32 *count);

    /**
     * @brief Просмотр таблицы базы данных лиц.
     *
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFeatureHubViewDBTable();

    /************************************************************************
     * Лицевая конвейерная обработка
     ************************************************************************/

    /**
     * @brief Обработка нескольких лиц в конвейере.
     *
     * Эта функция обрабатывает несколько лиц, обнаруженных на изображении или видеокадре, применяя
     * различные функции распознавания и анализа лиц в соответствии с заданными параметрами.
     *
     * @param session Дескриптор сеанса.
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param faces Указатель на структуру, содержащую данные о нескольких обнаруженных лицах.
     * @param parameter Пользовательские параметры для обработки лиц.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFMultipleFacePipelineProcess(HFSession session,
                                                                   HFImageStream streamHandle,
                                                                   PHFMultipleFaceData faces,
                                                                   HFSessionCustomParameter parameter);

    /**
     * @brief Обработка нескольких лиц в конвейере с дополнительной пользовательской опцией.
     *
     * Аналогично HFMultipleFacePipelineProcess, но позволяет использовать дополнительные пользовательские опции
     * для изменения поведения обработки лиц.
     *
     * @param session Дескриптор сеанса.
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param faces Указатель на структуру, содержащую данные о нескольких обнаруженных лицах.
     * @param customOption Целое число, представляющее пользовательскую опцию для обработки.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFMultipleFacePipelineProcessOptional(HFSession session,
                                                                           HFImageStream streamHandle,
                                                                           PHFMultipleFaceData faces,
                                                                           HInt32 customOption);

    /**
     * @brief Структура, представляющая уверенность в жизненности по RGB.
     *
     * Эта структура содержит количество лиц и уровень уверенности в определении жизненности
     * для каждого лица с использованием анализа RGB.
     */
    typedef struct HFRGBLivenessConfidence
    {
        HInt32 num;         ///< Количество обнаруженных лиц.
        HPFloat confidence; ///< Уровень уверенности в определении жизненности по RGB для каждого лица.
    } HFRGBLivenessConfidence, *PHFRGBLivenessConfidence;

    /**
     * @brief Получить уверенность в жизненности по RGB.
     *
     * Эта функция получает уровень уверенности в определении жизненности по RGB для лиц, обнаруженных
     * в текущем контексте.
     *
     * @param session Дескриптор сеанса.
     * @param confidence Указатель на структуру, в которой будут храниться данные уверенности в жизненности по RGB.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetRGBLivenessConfidence(HFSession session,
                                                                PHFRGBLivenessConfidence confidence);

    /**
     * @brief Структура, представляющая уверенность в определении наличия маски на лице.
     *
     * Эта структура содержит количество лиц и уровень уверенности в определении наличия маски
     * для каждого лица.
     */
    typedef struct HFFaceMaskConfidence
    {
        HInt32 num;         ///< Количество обнаруженных лиц.
        HPFloat confidence; ///< Уровень уверенности в определении наличия маски для каждого лица.
    } HFFaceMaskConfidence, *PHFFaceMaskConfidence;

    /**
     * @brief Получить уверенность в определении наличия маски на лице.
     *
     * Эта функция получает уровень уверенности в определении наличия маски для лиц, обнаруженных
     * в текущем контексте.
     *
     * @param session Дескриптор сеанса.
     * @param confidence Указатель на структуру, в которой будут храниться данные уверенности в определении наличия маски на лице.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceMaskConfidence(HFSession session,
                                                             PHFFaceMaskConfidence confidence);

    /**
     * @brief Структура, представляющая уверенность в предсказании качества лица.
     *
     * Эта структура содержит количество лиц и уровень уверенности в предсказании качества лица
     * для каждого лица.
     */
    typedef struct HFFaceQualityConfidence
    {
        HInt32 num;         ///< Количество обнаруженных лиц.
        HPFloat confidence; ///< Уровень уверенности в предсказании качества лица для каждого лица.
    } HFFaceQualityConfidence, *PHFFaceQualityConfidence;

    /**
     * @brief Получить уверенность в предсказании качества лица.
     *
     * Эта функция получает уровень уверенности в предсказании качества лица для лиц, обнаруженных
     * в текущем контексте.
     *
     * @param session Дескриптор сеанса.
     * @param confidence Указатель на структуру, в которой будут храниться данные уверенности в определении наличия маски на лице.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceQualityConfidence(HFSession session,
                                                                PHFFaceQualityConfidence confidence);

    /**
     * @brief Оценить качество лица на изображении.
     *
     * Эта функция оценивает качество обнаруженного лица, такое как его четкость и видимость.
     *
     * @param session Дескриптор сеанса.
     * @param singleFace Токен, представляющий одно лицо.
     * @param confidence Указатель на значение с плавающей запятой, в котором будет храниться уверенность в качестве.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFFaceQualityDetect(HFSession session, HFFaceBasicToken singleFace,
                                                         HFloat *confidence);

    /**
     * @brief Состояния лица в модуле взаимодействия.
     */
    typedef struct HFFaceIntereactionState
    {
        HInt32 num;                       ///< Количество обнаруженных лиц.
        HPFloat leftEyeStatusConfidence;  ///< Состояние левого глаза: уверенность, близкая к 1, означает открытый, близкая к 0, означает закрытый.
        HPFloat rightEyeStatusConfidence; ///< Состояние правого глаза: уверенность, близкая к 1, означает открытый, близкая к 0, означает закрытый.
    } HFFaceIntereactionState, *PHFFaceIntereactionState;

    /**
     * @brief Получить результаты предсказания взаимодействия лица.
     * @param session Дескриптор сеанса.
     * @param result Результаты предсказания состояния лица в модуле взаимодействия.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceIntereactionStateResult(HFSession session,
                                                                      PHFFaceIntereactionState result);

    /**
     * @brief Действия, обнаруженные в модуле взаимодействия с лицом.
     */
    typedef struct HFFaceIntereactionsActions
    {
        HInt32 num;        ///< Количество обнаруженных действий.
        HPInt32 normal;    ///< Нормальные действия.
        HPInt32 shake;     ///< Действия тряски.
        HPInt32 jawOpen;   ///< Действия открывания челюсти.
        HPInt32 headRiase; ///< Действия поднятия головы.
        HPInt32 blink;     ///< Действия моргания.
    } HFFaceIntereactionsActions, *PHFFaceIntereactionsActions;

    /**
     * @brief Получить результаты предсказания действий взаимодействия с лицом.
     * @param session Дескриптор сеанса.
     * @param actions Результаты предсказания действий лица в модуле взаимодействия.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceIntereactionActionsResult(
        HFSession session, PHFFaceIntereactionsActions actions);
    /**
     * @brief Структура, представляющая результаты предсказания атрибутов лица.
     *
     * Эта структура содержит расу, пол и возрастную категорию для обнаруженного лица.
     */
    typedef struct HFFaceAttributeResult
    {
        HInt32 num;   ///< Количество обнаруженных лиц.
        HPInt32 race; ///< Раса обнаруженного лица.
                      ///< 0: чернокожий;
                      ///< 1: азиат;
                      ///< 2: латиноамериканец/испанец;
                      ///< 3: житель Ближнего Востока;
                      ///< 4: белый;

        HPInt32 gender; ///< Пол обнаруженного лица.
                        ///< 0: женский;
                        ///< 1: мужской;

        HPInt32 ageBracket; ///< Возрастная категория обнаруженного лица.
                            ///< 0: 0-2 года;
                            ///< 1: 3-9 лет;
                            ///< 2: 10-19 лет;
                            ///< 3: 20-29 лет;
                            ///< 4: 30-39 лет;
                            ///< 5: 40-49 лет;
                            ///< 6: 50-59 лет;
                            ///< 7: 60-69 лет;
                            ///< 8: старше 70 лет;
    } HFFaceAttributeResult, *PHFFaceAttributeResult;

    /**
     * @brief Получить результаты предсказания атрибутов лица.
     *
     * Эта функция получает результаты предсказания атрибутов, таких как раса, пол и возрастная категория
     * для лиц, обнаруженных в текущем контексте.
     *
     * @param session Дескриптор сеанса.
     * @param results Указатель на структуру, в которой будут храниться результаты предсказания атрибутов лица.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFGetFaceAttributeResult(HFSession session,
                                                              PHFFaceAttributeResult results);

    /************************************************************************
     * Системная функция
     ************************************************************************/

    /**
     * @brief Структура, представляющая информацию о версии библиотеки InspireFace.
     */
    typedef struct HFInspireFaceVersion
    {
        int major; ///< Основной номер версии.
        int minor; ///< Номер минорной версии.
        int patch; ///< Номер патча.
    } HFInspireFaceVersion, *PHFInspireFaceVersion;

    /**
     * @brief Функция для запроса информации о версии библиотеки InspireFace.
     *
     * Эта функция получает информацию о версии библиотеки InspireFace.
     *
     * @param version Указатель на структуру, в которой будет храниться информация о версии.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFQueryInspireFaceVersion(PHFInspireFaceVersion version);

    /**
     * @brief Встроенный режим уровня логирования SDK
     * */
    typedef enum HFLogLevel
    {
        HF_LOG_NONE = 0, // Без логирования, отключает весь вывод логов
        HF_LOG_DEBUG,    // Уровень отладки для подробной системной информации, в основном полезной для разработчиков
        HF_LOG_INFO,     // Информационный уровень для общей системной информации о состоянии работы
        HF_LOG_WARN,     // Уровень предупреждений для некритичных проблем, требующих внимания
        HF_LOG_ERROR,    // Уровень ошибок для событий ошибок, которые могут позволить приложению продолжить работу
        HF_LOG_FATAL     // Уровень фатальных ошибок для серьезных событий ошибок, которые, вероятно, приведут к завершению работы приложения
    } HFLogLevel;

    /**
     * @brief Установить встроенный уровень логирования SDK. По умолчанию HF LOG DEBUG
     * */
    HYPER_CAPI_EXPORT extern HResult HFSetLogLevel(HFLogLevel level);

    /**
     * @brief Отключить функцию логирования. Как HFSetLogLevel(HF_LOG_NONE)
     * */
    HYPER_CAPI_EXPORT extern HResult HFLogDisable();

    /********************************DEBUG Utils****************************************/

    /**
     * @brief Отобразить поток изображений для целей отладки.
     *
     * Эта функция используется для отладки, позволяя визуализировать поток изображений
     * по мере его обработки. Это может быть полезно для понимания данных, поступающих
     * от камеры или источника изображения.
     *
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     */
    HYPER_CAPI_EXPORT extern void HFDeBugImageStreamImShow(HFImageStream streamHandle);

    /**
     * @brief Декодировать изображение из ImageStream и сохранить его на диск.
     *
     * Используется для проверки наличия проблем с кодеком изображения и быстрой диагностики ошибок.
     *
     * @param streamHandle Дескриптор данных буфера, представляющего компонент потока камеры.
     * @param savePath Путь, по которому будет записано изображение.
     * @return HResult, указывающий на успех или неудачу операции.
     */
    HYPER_CAPI_EXPORT extern HResult HFDeBugImageStreamDecodeSave(HFImageStream streamHandle,
                                                                  HPath savePath);

    /**
     * @brief Отобразить текущую статистику управления ресурсами.
     *
     * Эта функция выводит статистику о ресурсах, управляемых ResourceManager,
     * включая общее количество созданных и освобожденных сеансов и потоков изображений, а также
     * количество тех, которые еще не были освобождены. Это может быть использовано для целей отладки,
     * чтобы убедиться, что ресурсы правильно управляются и для выявления потенциальных утечек ресурсов.
     *
     * @return HResult, указывающий на успех или неудачу операции.
     *         Возвращает HSUCCEED, если статистика была успешно отображена,
     *         в противном случае может вернуть код ошибки, если возникла проблема с доступом к менеджеру ресурсов.
     */
    HYPER_CAPI_EXPORT extern HResult HFDeBugShowResourceStatistics();

#ifdef __cplusplus
}
#endif

#endif // HYPERFACEREPO_INSPIREFACE_H