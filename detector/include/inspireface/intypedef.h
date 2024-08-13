//
// Создано tunm 03.10.2023.
//

#ifndef HYPERFACEREPO_INTYPEDEF_H
#define HYPERFACEREPO_INTYPEDEF_H

typedef void *HPVoid;         ///< Указатель на Void.
typedef void *HFImageStream;  ///< Дескриптор для изображения.
typedef void *HFSession;      ///< Дескриптор для контекста.
typedef long HLong;           ///< Длинное целое.
typedef float HFloat;         ///< Одинарная точность с плавающей запятой.
typedef float *HPFloat;       ///< Указатель на число с одинарной точностью с плавающей запятой.
typedef double HDouble;       ///< Двойная точность с плавающей запятой.
typedef unsigned char HUInt8; ///< Беззнаковое 8-битное целое.
typedef signed int HInt32;    ///< Знаковое 32-битное целое.
typedef signed int HOption;   ///< Знаковый 32-битный целочисленный параметр.
typedef signed int *HPInt32;  ///< Указатель на знаковое 32-битное целое.
typedef long HResult;         ///< Код результата.
typedef char *HString;        ///< Строка.
typedef const char *HPath;    ///< Константная строка.
typedef char HBuffer;         ///< Символ.
typedef char *HPBuffer;       ///< Указатель на символ.
typedef long HSize;           ///< Размер
typedef long *HPSize;         ///< Указатель на размер

typedef struct HFaceRect
{
    HInt32 x;      ///< X-координата верхнего левого угла прямоугольника.
    HInt32 y;      ///< Y-координата верхнего левого угла прямоугольника.
    HInt32 width;  ///< Ширина прямоугольника.
    HInt32 height; ///< Высота прямоугольника.
} HFaceRect;       ///< Прямоугольник, представляющий область лица.

typedef struct HPoint2f
{
    HFloat x; ///< X-координата
    HFloat y; ///< Y-координата
} HPoint2f;

#endif // HYPERFACEREPO_INTYPEDEF_H
