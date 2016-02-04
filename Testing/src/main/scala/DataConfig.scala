package org.template.classification

case class DataConfig() {
    val attrCount = 12
    val attrArray = Range(0, attrCount).map(t => t.toString()).toArray
}