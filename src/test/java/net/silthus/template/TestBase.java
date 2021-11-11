package net.silthus.template;

import be.seeseemelk.mockbukkit.MockBukkit;
import be.seeseemelk.mockbukkit.ServerMock;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;

public abstract class TestBase {

    protected ServerMock server;
    protected TemplatePlugin plugin;

    @BeforeEach
    public void setUp() {
        server = MockBukkit.mock();
        plugin = MockBukkit.load(TemplatePlugin.class);
    }

    @AfterEach
    public void tearDown() {
        MockBukkit.unmock();
    }
}
