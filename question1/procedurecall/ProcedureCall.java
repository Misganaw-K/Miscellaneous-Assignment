
package procedurecall;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

/**
 *
 * @author Misganaw
 */
public class ProcedureCall {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
      try
        {
            // Create an object of the interface
            // implementation class
            Search obj = new SearcQuery();
 
            // rmiregistry within the server JVM with
            // port number 1900
            LocateRegistry.createRegistry(1900);
 
            // Binds the remote object by the name
            // geeksforgeeks
            Naming.rebind("rmi://localhost:1900"+
                          "/geeksforgeeks",obj);
        }
        catch(Exception ae)
        {
            System.out.println(ae);
        }
    }
    
}
