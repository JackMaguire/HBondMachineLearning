public class test{

    public static void main(String[] args){

    }

    public static boolean test_table_io(){
	try {

	    

	} catch( Exception e ){
	    System.err.println( e.getMessage() );
	    return false;
	}
	return true;
    }


    public static boolean test_binForValue(){
	try {
	    final MinMax range = new MinMax( -200, 50 );

	} catch ( Exception e ) {
	    System.err.println( e.getMessage() );
	    return false;
	}
	return true;
    }






    private static void ASSERT( boolean in ) throws Exception{
	if( ! in ){
	    throw new Exception();
	}
    }

    private static void ASSERT_EQUALS( Object a, Object b ) throws Exception{
	if( a != b ){
	    throw new Exception( a + " != " + b );
	}
    }


}

