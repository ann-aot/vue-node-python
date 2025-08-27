// Example custom command
Cypress.Commands.add("visitHome", () => {
  cy.visit("/");
});
