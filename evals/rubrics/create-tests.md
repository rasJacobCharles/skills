# create-tests Eval Rubric

Score each criterion **PASS (1)** / **FAIL (0)** / **N/A**.
N/A criteria are excluded from the denominator.
Final score = sum(PASS) / sum(applicable) × 100.

Sources: [PHPUnit 13.1 docs](https://docs.phpunit.de/en/13.1/) and `SKILL.md`.

---

## 1. File Structure (6 pts)
*   **1.1** `declare(strict_types=1)` is present (verify via grep/read)
*   **1.2** Test class is `final` (verify via grep/read)
*   **1.3** Correct base class — unit → `TestCase`, integration → `AppTestCase` (verify via read)
*   **1.4** Namespace mirrors source path (verify via read)
*   **1.5** No inline FQCNs — all classes imported via `use` (verify via grep for `\` inside method bodies)
*   **1.6** No `setUp()` unless there is genuinely shared state across every test (verify via read)

## 2. Attributes (7 pts)
*   **2.1** `#[Test]` on every test method (verify via grep)
*   **2.2** No `test` prefix on method names (verify via grep for `public function test`)
*   **2.3** `#[CoversClass(Foo::class)]` on the test class (verify via grep)
*   **2.4** `#[Group(...)]` on the test class (verify via grep)
*   **2.5** `#[TestDox]` used where method name alone is not a readable spec sentence (verify via read)
*   **2.6** `#[DataProvider]` or `#[TestWith]` used when multiple scenarios exist instead of duplicated methods (verify via read)
*   **2.7** `#[DoesNotPerformAssertions]` used on tests that intentionally have no assertions (verify via read)

## 3. Tier Selection (1 pt)
*   **3.1** Correct tier chosen — unit for isolated services/formatters, integration for handlers/container-dependent classes (verify via read)

## 4. Mocking Discipline (6 pts)
*   **4.1** Only `createMock()` / `createStub()` — no `getMockBuilder()`, `onlyMethods()`, partial mocks (verify via grep)
*   **4.2** `createStub()` used for pure stubs (no `expects()` call on them) (verify via read)
*   **4.3** `createMock()` + `expects($this->once())` used when verifying a call is made (verify via read)
*   **4.4** No `expects($this->any())` — stubs have no `expects()` at all (verify via grep)
*   **4.5** No framework/infrastructure classes mocked (no mocking `ServerRequestInterface`, `View`, PDO, etc.) (verify via read)
*   **4.6** No model/entity classes mocked — real instances used (via factories where available) (verify via read)

## 5. Assertions (7 pts)
*   **5.1** `assertSame` used for scalar/value comparisons (not `assertEquals`) (verify via grep)
*   **5.2** `assertCount($n, $x)` used — not `assertSame($n, count($x))` or `assertEquals($n, count($x))` (verify via grep)
*   **5.3** `assertNull` / `assertNotNull` used — not `assertSame(null, ...)` (verify via grep)
*   **5.4** `assertTrue` / `assertFalse` used — not `assertSame(true/false, ...)` (verify via grep)
*   **5.5** `assertEmpty` not used (verify via grep)
*   **5.6** `expectExceptionObject(new Foo())` used for exception tests — not two-line `expectException` + `expectExceptionMessage` (verify via grep)
*   **5.7** `assertInstanceOf` called first when drilling into a returned object (verify via read)

## 6. AAA Pattern (4 pts)
*   **6.1** `// ARRANGE`, `// ACT`, `// ASSERT` comments present in uppercase (verify via grep)
*   **6.2** Exactly one blank line between sections — no blank lines within a section (verify via read)
*   **6.3** `// ACT && ASSERT` used when `expectException*` precedes the call (not separate sections) (verify via read)
*   **6.4** No conditional logic in tests — no `if`, `foreach` over assertions, no `try/catch` around the act step (verify via grep)

## 7. Data Providers (3 pts — N/A if no multi-scenario method)
*   **7.1** Provider method is `public static` with `iterable` return type (verify via grep)
*   **7.2** Named `yield` keys used (`yield 'paid order' => [...]`) (verify via grep)
*   **7.3** No duplicated test methods covering the same logic — consolidated into one `#[DataProvider]` test (verify via read)

## 8. One Behaviour Per Test (2 pts)
*   **8.1** Each test method covers exactly one scenario or code path (verify via read)
*   **8.2** No `#[Depends]` — tests are independent (verify via grep)
