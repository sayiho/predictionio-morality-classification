package org.template.classification

case class DataConfig() {
    val attrCount = 12
    val attrArray = Range(0, attrCount).map(t => t.toString()).toArray
    val featureNames = Array(
        "x36",
        "x37",
        "x59",
        "x151",
        "x167",
        "x175",
        "x198",
        "x226",
        "x322",
        "x325",
        "x480",
        "x476"
    )
    val default: Array[Double] = Array(
        6.166249999999992,
        5.880863039399625,
        3.4523076923076936,
        4.518482293423271,
        7.552420289855071,
        3.7854125412541246,
        4.49621052631579,
        6.898714524207007,
        1.546162402669633,
        1.5321729957805907,
        18.10611510791367,
        69.318359375
    )
}