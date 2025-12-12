from infra.vpn_panel.remnwave_gateway import RemnawaveGateway
import asyncio

remnawave_gateway = RemnawaveGateway()
asyncio.run(remnawave_gateway.create_panel_user())
