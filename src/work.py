import asyncio
from src.socket_service import SocketService
from src.models.requests import WorkUnit
from dummy_response import audit

from src.smart_contracts.dependency_tree import DependencyTree

from src.analysis.model import MODEL


# TODO: If the UI never connects persist the result for sometime
# and return it when the UI tries to connect
async def process_work(work: WorkUnit):
    await asyncio.sleep(0.5)
    await SocketService.send({"status": "building_dt"})
    dt = DependencyTree(work)
    print("Built dependency tree")
    main_ids = dt.get_main_ids()

    for idx, id in enumerate(main_ids):
        await SocketService.send(
            {
                "status": "analyzing",
                "progress": {"current": idx + 1, "total": len(main_ids)},
            }
        )
        codeblocks = dt.tree(id)
        input = codeblocks["main"] + "\n\n" + "\n\n".join(codeblocks["dependencies"])
        output = MODEL.analyze(input)
        print(output)

    await SocketService.send({"status": "complete", "done": True, "result": output})
    await SocketService.close()
