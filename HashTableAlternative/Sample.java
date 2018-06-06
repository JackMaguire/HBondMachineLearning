public class Sample {

    public int num_data_points;
    public int num_positive_data_points;

    public Sample(){
	num_data_points = 0;
	num_positive_data_points = 0;
    }

    public Sample( Sample src ){
	num_data_points = src.num_data_points;
	num_positive_data_points = src.num_positive_data_points;
    }

}
