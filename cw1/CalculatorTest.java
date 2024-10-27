
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {

    private final Calculator calculator = new Calculator();

    @Test
    void testAdd() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    void testSubtract() {
        assertEquals(1, calculator.subtract(5, 4));
    }

    @Test
    void testSubtractWithNegativeNumbers() {
        assertEquals(7, calculator.subtract(3, -4));
        assertEquals(1, calculator.subtract(-3, -4));
    }

    @Test
    void testMultiply() {
        assertEquals(20, calculator.multiply(4, 5));
    }

    @Test
    void testDivide() {
        assertEquals(2.0, calculator.divide(10, 5));
    }

    @Test
    void testDivideDoubles() {
        assertEquals(2.5, calculator.divide(5, 2), 0.0001); // delta to tolerancja .
        assertNotEquals(2.6, calculator.divide(5, 2), 0.0001);
    }
// inne asercje:
    @Test
    void testDivideByZero() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            calculator.divide(10, 0);
        });
        assertEquals("Division by zero is not allowed.", exception.getMessage());
    }


    @Test
    void testAddIntegersNotEqual() {

        assertNotEquals(8, calculator.add(3, 4));
    }

    @Test
    void testCalculatorNotNull() {
        assertNotNull(calculator); // Kalkulator nie powinien być nullem
    }

    @Test
    void testAdditionPositiveResult() {
        assertTrue(calculator.add(2, 3) > 0);
        assertFalse(calculator.add(3,7)<0);
    }

}
