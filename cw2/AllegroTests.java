import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.List;

public class AllegroTests {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    public void setUp() {
        // Ustawienie ścieżki do Geckodrivera
        System.setProperty("webdriver.gecko.driver", "geckodriver.exe");
        driver = new FirefoxDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.manage().window().maximize();
        driver.get("https://allegro.pl/");
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    public void testPageTitle() {
        // Asercja 1: Sprawdzenie tytułu strony
        String title = driver.getTitle();
        assertTrue(title.contains("Allegro"), "Tytuł strony nie zawiera 'Allegro'");
    }

    @Test
    public void testSearchFunctionality() {
        // Asercja 2: Wyszukiwanie produktu i sprawdzenie wyników
        WebElement searchBox = driver.findElement(By.name("string"));
        searchBox.sendKeys("Laptop");
        searchBox.submit();

        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("[data-role='product']")));
        List<WebElement> results = driver.findElements(By.cssSelector("[data-role='product']"));
        assertTrue(results.size() > 0, "Brak wyników wyszukiwania dla 'Laptop'");
    }

    @Test
    public void testCategoryNavigation() {
        // Asercja 3: Sprawdzenie nawigacji po kategoriach
        WebElement categoryButton = driver.findElement(By.cssSelector("button[data-role='menu-button']"));
        categoryButton.click();

        WebElement electronicsCategory = wait.until(ExpectedConditions.elementToBeClickable(By.linkText("Elektronika")));
        electronicsCategory.click();

        String currentUrl = driver.getCurrentUrl();
        assertTrue(currentUrl.contains("kategoria-elektronika"), "Nawigacja do kategorii Elektronika nie działa poprawnie");
    }

    @Test
    public void testAddToFavorites() {
        // Asercja 4: Dodanie produktu do ulubionych
        WebElement firstProduct = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("[data-role='product']")));
        firstProduct.click();

        WebElement favoriteButton = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button[data-role='favorite-button']")));
        favoriteButton.click();

        WebElement confirmationMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".confirmation-message")));
        assertNotNull(confirmationMessage, "Produkt nie został dodany do ulubionych");
    }

    @Test
    public void testLoginFormDisplayed() {
        // Asercja 5: Sprawdzenie wyświetlenia formularza logowania
        WebElement loginButton = driver.findElement(By.cssSelector("[data-role='login-button']"));
        loginButton.click();

        WebElement loginForm = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("form#login-form")));
        assertTrue(loginForm.isDisplayed(), "Formularz logowania nie jest wyświetlony");
    }

    @Test
    public void testFooterLinks() {
        // Asercja 6: Sprawdzenie, czy linki w stopce są dostępne
        List<WebElement> footerLinks = driver.findElements(By.cssSelector("footer a"));
        assertTrue(footerLinks.size() > 0, "Brak linków w stopce");
    }

    @Test
    public void testCartEmpty() {
        // Asercja 7: Sprawdzenie, czy koszyk jest pusty po wejściu
        WebElement cartButton = driver.findElement(By.cssSelector("[data-role='cart-button']"));
        cartButton.click();

        WebElement emptyCartMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".empty-cart-message")));
        assertTrue(emptyCartMessage.isDisplayed(), "Koszyk nie jest pusty");
    }

    @Test
    public void testCookiesBanner() {
        // Asercja 8: Sprawdzenie obecności banera cookies
        WebElement cookiesBanner = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".cookies-banner")));
        assertTrue(cookiesBanner.isDisplayed(), "Baner cookies nie jest widoczny");
    }
}
