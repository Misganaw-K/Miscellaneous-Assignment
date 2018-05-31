
package procedurecall;

import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 *
 * @author Misganaw
 */
public interface Search  extends Remote{
    // Declaring the method prototype
    public String query(String search) throws RemoteException;
    
}
