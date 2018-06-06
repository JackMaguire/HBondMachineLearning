public class test{

    public static void main(String[] args){

	System.out.println( "test_table_io(): " + test_table_io( false ) );
	System.out.println( "test_binForValue(): " + test_binForValue( false ) );

    }

    public static boolean test_table_io( boolean verbose ){
	try {

	    

	} catch( Exception e ){
	    System.err.println( e.getMessage() );
	    return false;
	}
	return true;
    }


    public static boolean test_binForValue( boolean verbose ){
	try {
	    final MinMax range = new MinMax( -200, 50 );

	    for( int bins = 1; bins < 10; bins += 3 ){
		ASSERT_EQUALS( Table.binForValue( -200, range, bins ), 0 );
		ASSERT_EQUALS( Table.binForValue(   50, range, bins ), bins - 1 );
	    }

	    for( int bins = 1; bins < 10; bins += 3 ){
		ASSERT_EQUALS( Table.binForValue( -199, range, bins ), 0 );
		ASSERT_EQUALS( Table.binForValue(   49, range, bins ), bins - 1 );
	    }

	    if( verbose ){
		final MinMax range2 = new MinMax( 0, 10 );
		for( double x = -0.5; x < 11.0; x += 0.5 ){
		    System.out.println( x + " " + Table.binForValue( x, range2, 3 ) );
		}
	    }

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

