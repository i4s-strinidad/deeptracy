@only
Feature: RetireJS Plugin
  RetireJS Plugin should work as expected

  Background: Database setup
    Given a clean system
    And a plugin for "retirejs" exists in the plugin table for lang "nodejs"
    And a project with "https://github.com/jspm/registry.git" repo exists in the database
    And a scan for lang "nodejs" exists for the project

  Scenario: The plugin generates valid output
    When a task for "prepare_scan" is added to celery for the scan
    And all celery tasks are done
    Then the scan folder is deleted
    And 1 scan analysis is generated in the database
    And the results for the analysis in the database exists
    And the scan analysis_done is equals analysis_count
    And the scan state is DONE
    # And the results for the scan in the database exists
