describe('CHEFS Vue Template - Home Page', () => {
    beforeEach(() => {
        cy.visit('/'); // loads Home page
    });

    it('loads the homepage', () => {
        cy.get('#app').should('exist'); // root container
    });

    it('displays the Vite logo', () => {
        cy.get('img[alt="Vite logo"]').should('be.visible');
    });

    it('displays the Vue logo', () => {
        cy.get('img[alt="Vue logo"]').should('be.visible');
    });

    it('renders HelloWorld component with correct message', () => {
        cy.contains('Vite + Vue').should('be.visible');
    });
});
