public class MinMax {
    public double min;
    public double max;

    public MinMax(){
	min = 99999;
	max = -99999;
    }

    public MinMax( MinMax src ){
	min = src.min;
	max = src.max;
    }
}
