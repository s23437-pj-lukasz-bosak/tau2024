import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

import static org.junit.Assert.*;

public class AmazonTest {
    private WebDriver driver;

    @Before
    public void setUp() {
        System.setProperty("webdriver.gecko.driver", "geckodriver.exe");
        driver = new FirefoxDriver();
    }

    @Test
    public void testAmazonHomePage() {
        // Otwórz stronę Amazon
        driver.get("https://www.amazon.com");

        // Utwórz WebDriverWait do dynamicznego oczekiwania
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        // Asercja 1: Sprawdź, czy tytuł strony zawiera "Amazon"
        String title = driver.getTitle();
        assertTrue("Tytuł strony powinien zawierać 'Amazon'", title.contains("Amazon"));

        // Asercja 2: Sprawdź, czy logo Amazonu jest widoczne
        WebElement logo = driver.findElement(By.id("nav-logo-sprites"));
        assertTrue("Logo Amazonu powinno być widoczne", logo.isDisplayed());

        // Asercja 3: Sprawdź, czy pole wyszukiwania jest widoczne
        WebElement searchInput = driver.findElement(By.id("twotabsearchtextbox"));
        assertTrue("Pole wyszukiwania powinno być widoczne", searchInput.isDisplayed());

        // Asercja 4: Sprawdź, czy przycisk wyszukiwania jest widoczny
        WebElement searchButton = driver.findElement(By.id("nav-search-submit-button"));
        assertTrue("Przycisk wyszukiwania powinien być widoczny", searchButton.isDisplayed());

        // Wykonaj wyszukiwanie dla frazy "Selenium WebDriver book"
        searchInput.sendKeys("Selenium WebDriver book");
        searchButton.click();

        // Poczekaj na załadowanie wyników wyszukiwania
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("span.a-size-medium")));

        // Asercja 5: Sprawdź, czy tytuł strony wyników wyszukiwania zawiera "Selenium WebDriver book"
        String resultsTitle = driver.getTitle();
        assertTrue("Tytuł strony wyników wyszukiwania powinien zawierać 'Selenium WebDriver book'", resultsTitle.contains("Selenium WebDriver book"));

        // Asercja 6: Sprawdź, czy na stronie wyników wyszukiwania jest lista produktów
        List<WebElement> productTitles = driver.findElements(By.cssSelector("span.a-size-medium"));
        assertTrue("Powinno być co najmniej kilka produktów na liście wyników wyszukiwania", productTitles.size() > 0);

        // Asercja 7: Sprawdź, czy pierwszy wynik ma widoczny tytuł
        WebElement firstProductTitle = productTitles.get(0);
        assertNotNull("Pierwszy wynik powinien mieć tytuł", firstProductTitle.getText());

        // Asercja 8: Sprawdź, czy pierwszy wynik ma widoczną cenę (jeśli jest dostępna)
        WebElement firstProductPrice = driver.findElement(By.cssSelector("span.a-price-whole"));
        assertTrue("Cena pierwszego wyniku powinna być widoczna", firstProductPrice.isDisplayed());
    }

    @After
    public void tearDown() {
        // Zamknij przeglądarkę po teście
        if (driver != null) {
            driver.quit();
        }
    }
}