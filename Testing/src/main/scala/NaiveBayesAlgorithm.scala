package org.template.classification

import io.prediction.controller.P2LAlgorithm
import io.prediction.controller.Params

import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.classification.NaiveBayesModel
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.SparkContext

import grizzled.slf4j.Logger

case class AlgorithmParams(
  lambda: Double
) extends Params

// extends P2LAlgorithm because the MLlib's NaiveBayesModel doesn't contain RDD.
class NaiveBayesAlgorithm(val ap: AlgorithmParams)
  extends P2LAlgorithm[PreparedData, NaiveBayesModel, Query, PredictedResult] {

  @transient lazy val logger = Logger[this.type]

  def train(sc: SparkContext, data: PreparedData): NaiveBayesModel = {
    // MLLib NaiveBayes cannot handle empty training data.
    require(data.labeledPoints.take(1).nonEmpty,
      s"RDD[labeledPoints] in PreparedData cannot be empty." +
      " Please check if DataSource generates TrainingData" +
      " and Preparator generates PreparedData correctly.")

    NaiveBayes.train(data.labeledPoints, ap.lambda)
  }

  val config = DataConfig()

  def predict(model: NaiveBayesModel, query: Query): PredictedResult = {
    val features = new Array[Double](query.features.length)
    var i = 0
    while (i < query.features.length) {
      features(i) = if (query.features(i) == -1) config.default(i) else query.features(i)
      i += 1
    }
    val label = model.predict(Vectors.dense(
      features
    ))
    val probabilities = model.predictProbabilities(Vectors.dense(
      features
    ))
    new PredictedResult(label, null, probabilities, model.modelType)
  }

}
