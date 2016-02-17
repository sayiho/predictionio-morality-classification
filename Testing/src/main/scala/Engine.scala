package org.template.classification

import org.apache.spark.mllib.linalg.DenseVector

import io.prediction.controller.EngineFactory
import io.prediction.controller.Engine

class Query(
  val features: Array[Double]
) extends Serializable {
  def getFeature(name: String) {
    features(name.toInt)
  }
}

class PredictedResult(
  val label: Double,
  val query: Query,
  val probabilities: DenseVector
) extends Serializable {
  def this(label: Double) = this(label, null, null)
}

class ActualResult(
  val label: Double
) extends Serializable

object ClassificationEngine extends EngineFactory {
  def apply() = {
    new Engine(
      classOf[DataSource],
      classOf[Preparator],
      Map("naive" -> classOf[NaiveBayesAlgorithm]),
      classOf[Serving])
  }
}
