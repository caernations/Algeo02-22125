from PIL import Image
import math
import os


def main():
    imagePATH = "./image/image.jpg"  # Path to image (directly to image.jpg)
    datasetPATH = "./dataset"  # Path to dataset folder
    datasetFiles = os.listdir(datasetPATH)

    listDatasets = [None for _ in range(len(datasetFiles))]

    for i in range(len(datasetFiles)):
        listDatasets[i] = Image.open(os.path.join(datasetPATH, datasetFiles[i]))

        listDatasets[i] = listDatasets[i].convert("L")

        width, height = listDatasets[i].size

        listDatasets[i] = list(
            Image.open(os.path.join(datasetPATH, datasetFiles[i])).getdata()
        )

        listDatasets[i] = [
            listDatasets[i][n : n + width]
            for n in range(0, len(listDatasets[i]), width)
        ]

        image = Image.open(imagePATH)  # Image variable
        image = image.convert("L")

        width, height = image.size

        pixelMatrix = list(image.getdata())
        pixelMatrix = [
            pixelMatrix[n : n + width] for n in range(0, len(pixelMatrix), width)
        ]

        listTextureResult = [None for _ in range(len(listDatasets))]
        for i in range(len(listDatasets)):
            listTextureResult[i] = cosineSimilarityTexture(pixelMatrix, listDatasets[i])

        print(listTextureResult)


def GLCM(image):
    height = len(image)
    width = len(image[0])
    frameworkMatrix = [[0 for _ in range(256)] for _ in range(256)]

    for i in range(height):
        for j in range(width - 1):
            idxI = image[i][j]
            idxJ = image[i][j + 1]
            frameworkMatrix[idxI][idxJ] += 1
    transposeFramework = transposeMatrix(frameworkMatrix)

    for i in range(256):
        for j in range(256):
            frameworkMatrix[i][j] += transposeFramework[i][j]

    glcm = normaliseSymmetricMatrix(frameworkMatrix)
    return glcm


def metric(image):
    contrast = 0
    homogeneity = 0
    dissimilarity = 0
    asm = 0
    energy = 0
    glcm = GLCM(image)
    for i in range(255):
        for j in range(255):
            contrast += glcm[i][j] * ((i - j) ** 2)
            homogeneity += (glcm[i][j]) / (1 + ((i - j) ** 2))
            dissimilarity += (glcm[i][j] * abs((i-j)))
            asm += ((glcm[i][j]) ** 2)
    energy = math.sqrt(asm)
    return contrast, homogeneity, dissimilarity, asm, energy


def cosineSimilarityTexture(image1, image2):
    c1, h1, d1, a1, e1 = metric(image1)
    c2, h2, d2, a2, e2 = metric(image2)

    dotProductC = sum(a * b for a, b in zip(c1, c2))
    magnitudeC1 = math.sqrt(sum(a**2 for a in c1))
    magnitudeC2 = math.sqrt(sum(b**2 for b in c2))
    resultC = dotProductC / (magnitudeC1 * magnitudeC2)

    dotProductH = sum(a * b for a, b in zip(h1, h2))
    magnitudeH1 = math.sqrt(sum(a**2 for a in h1))
    magnitudeH2 = math.sqrt(sum(b**2 for b in h2))
    resultH = dotProductH / (magnitudeH1 * magnitudeH2)

    dotProductD = sum(a * b for a, b in zip(d1, d2))
    magnitudeD1 = math.sqrt(sum(a**2 for a in d1))
    magnitudeD2 = math.sqrt(sum(b**2 for b in d2))
    resultD = dotProductD / (magnitudeD1 * magnitudeD2)

    dotProductA = sum(a * b for a, b in zip(a1, a2))
    magnitudeA1 = math.sqrt(sum(a**2 for a in a1))
    magnitudeA2 = math.sqrt(sum(b**2 for b in a2))
    resultA = dotProductA / (magnitudeA1 * magnitudeA2)

    dotProductE = sum(a * b for a, b in zip(e1, e2))
    magnitudeE1 = math.sqrt(sum(a**2 for a in e1))
    magnitudeE2 = math.sqrt(sum(b**2 for b in e2))
    resultE = dotProductE / (magnitudeE1 * magnitudeE2)

    overallResult = (resultC + resultH + resultD + resultA + resultE) / 5

    return overallResult


def transposeMatrix(matrix):
    return [list(i) for i in zip(*matrix)]


def sumElmtMatrix(matrix):
    sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            sum += matrix[i][j]
    return sum


def normaliseSymmetricMatrix(matrix):
    sum = sumElmtMatrix(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] /= sum
    return matrix


if __name__ == "__main__":
    main()
