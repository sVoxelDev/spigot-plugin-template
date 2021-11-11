package net.silthus.template;

import be.seeseemelk.mockbukkit.MockBukkit;
import be.seeseemelk.mockbukkit.ServerMock;
import net.milkbowl.vault.economy.Economy;
import net.silthus.template.integrations.vault.VaultProvider;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;

import static org.mockito.Mockito.mock;

public abstract class TestBase {

    protected ServerMock server;
    protected TemplatePlugin plugin;
    protected Economy economy;

    @BeforeEach
    public void setUp() {
        server = MockBukkit.mock();
        plugin = MockBukkit.load(TemplatePlugin.class);
        mockVaultEconomy();
    }

    private void mockVaultEconomy() {
        economy = mock(Economy.class);
        plugin.setVault(new VaultProvider(economy));
    }

    @AfterEach
    public void tearDown() {
        MockBukkit.unmock();
    }
}
