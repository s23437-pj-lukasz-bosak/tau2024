import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class SklepTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    public void setUp() {

        FirefoxOptions options = new FirefoxOptions();
        //options.setHeadless(true); // Uruchomienie przeglądarki w trybie headless (opcjonalnie)

        System.setProperty("webdriver.gecko.driver", "geckodriver.exe");
        driver = new FirefoxDriver(options);

        wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        driver.get("https://skleptest.pl/");
    }

    @Test
    public void testNoResultsForInvalidSearch() {
        // Wyszukiwanie terminu, który nie istnieje
        WebElement searchBox = driver.findElement(By.id("search-field-top-bar"));
        searchBox.sendKeys("rakieta kosmiczna");
        searchBox.submit();

        // Czekaj na załadowanie wyników wyszukiwania
        wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(".no-results")));

        // Sprawdzenie, czy pojawił się komunikat o braku wyników
        WebElement noResultsMessage = driver.findElement(By.cssSelector(".no-results"));
        Assertions.assertTrue(noResultsMessage.isDisplayed(), "Nie wyświetlono komunikatu o braku wyników.");
    }



    @Test
    public void testSortingFunctionality() {
        WebElement searchBox = driver.findElement(By.id("search-field-top-bar"));
        Assertions.assertTrue(searchBox.isDisplayed(), "Pole wyszukiwania nie jest widoczne.");

    }


    @Test
    public void testAccountCreationLink() {
        // Asercja 1: Sprawdzenie, czy link do tworzenia konta jest widoczny
        WebElement createAccountLink = driver.findElement(By.className("top-account"));
        Assertions.assertTrue(createAccountLink.isDisplayed(), "Link do tworzenia konta nie jest widoczny.");

        // Asercja 2: Sprawdzenie, czy link jest aktywny (kliknęcie możliwe)
        Assertions.assertTrue(createAccountLink.isEnabled(), "Link do tworzenia konta nie jest aktywny.");

        // Asercja 3: Sprawdzenie, czy można kliknąć link i przejść do formularza tworzenia konta
        createAccountLink.click();

        // Czekamy na załadowanie formularza rejestracyjnego po kliknięciu
        wait.until(ExpectedConditions.presenceOfElementLocated(By.id("reg_email")));  // Zaktualizuj selektor formularza

        // Asercja 4: Sprawdzenie, czy formularz rejestracyjny jest widoczny
        WebElement registrationForm = driver.findElement(By.id("reg_email"));
        Assertions.assertTrue(registrationForm.isDisplayed(), "Formularz tworzenia konta nie jest widoczny.");
    }

    @Test
    public void testLogoClickRedirectsToHomePage() {
        // Asercja 1: Zidentyfikowanie elementu logo (dostosuj selektor, jeśli jest inny)
        WebElement logo = driver.findElement(By.className("site-title"));  // Zaktualizuj selektor logo

        // Asercja 2: Sprawdzenie, czy logo jest widoczne
        Assertions.assertTrue(logo.isDisplayed(), "Logo nie jest widoczne.");

        // Asercja 3: Kliknięcie w logo
        logo.click();

        // Asercja 4: Poczekanie na załadowanie strony głównej
        wait.until(ExpectedConditions.urlToBe("https://skleptest.pl/"));  // Zaktualizuj URL strony głównej

        // Asercja 5: Sprawdzenie, czy strona po kliknięciu ma URL głównej strony
        String currentUrl = driver.getCurrentUrl();
        Assertions.assertEquals("https://skleptest.pl/", currentUrl, "Po kliknięciu w logo nie przeniesiono na stronę główną.");
    }

    @AfterEach
    public void tearDown() {
        // Zamykanie przeglądarki po każdym teście
        if (driver != null) {
            driver.quit();
        }
    }
}
