Feature: Example Acceptance Test
  Player receives an item when executing a command.

  Background:
    Given I joined the server

  Scenario: Player is greeted when joining the server
    Given I joined the server
    Then I receive the message: "Welcome to our server!"

  @Ignore
  Scenario: User can perform command and receives item
    Given I have the "template.player.diamonds" permission
    When I execute '/template diamonds'
    Then I get 64 diamond
