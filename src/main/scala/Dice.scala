import scala.util.Random

object Dice {
  val trick = Array(1,4,4,4,4,4)
  val defend = Array(3,3,3,3,3,6)
  val attack = Array(2,2,2,5,5,5)

  def roll(d: Array[Int]): Int = {
    d(Random.nextInt(d.length))
  }

  def roll(d: Array[Int], pool: Int): Int = {
    (1 to pool).map(_ => roll(d)).reduce(math.max)
  }

  def value(d1: Array[Int], pool1: Int, str1: Int, d2: Array[Int], pool2: Int, str2: Int, reps: Int): Double = {
    val total = (1 to reps).map{_ =>
      val r1 = roll(d1, pool1)
      val r2 = roll(d2, pool2)
      if ( r1 > r2 ) str1 else if (r1 == r2) 0 else -str2
    }.sum
    total.toDouble / reps
  }

  def riskValue(d1: Array[Int], pool1: Int, str1: Int, d2: Array[Int], pool2: Int, str2: Int, reps: Int): Double = {
    val total = (1 to reps).map{_ =>
      val r1 = roll(d1, pool1)
      val r2 = roll(d2, pool2)
      if ( r1 > r2 ) str1 else if (r1 == r2) 0 else -str2 - (str1 - 1)
    }.sum
    total.toDouble / reps
  }


  def flex(d1: Array[Int], pool1: Int, str1: Int, d1b: Array[Int], pool1b: Int, str1b: Int, d2: Array[Int], pool2: Int, str2: Int, reps: Int): Double = {
    val total = (1 to reps).map{_ =>
      val r1 = roll(d1, pool1)
      val r1b = roll(d1b, pool1b) 
      val r2 = roll(d2, pool2)

      (r1 > r2, r1b > r2) match {
        case (false, false) => -str2
        case (true, false) => str1
        case (false, true) => str1b
        case (true, true) => math.max(str1, str1b)
      }
    }.sum
    total.toDouble / reps
  }
  

  def matrix(pool: Int, str: Int) = {
    val all = Array(("trick", trick), ("defend", defend), ("attack", attack))
    for {
      (n1, d1) <- all
      (n2, d2) <- all
    } yield s"$n1 v $n2 ${value(d1, pool, str, d2, pool, str, 100000)}"
  }
}
