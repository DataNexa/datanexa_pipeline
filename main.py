"""
/***********************************************************************
 *                          Desenvolvido por:                          *
 *                                                                     *
 *                       ┏━━━┓━━┳━━━━┓━━━┓━━┓━┓                        *
 *                       ┃ ┏┓┃ ┃┃┃ ┓┓┃┃━┓┃ ┳┛ ┃                        *
 *                       ┃ ┣┃┃ ┃┃┃ ┻┛┃┃━┓┃ ┻┓ ┃                        *
 *                       ┗━┛┗┛━┻━┛━━━┛━ ┗┗━━┛━┛                        *
 *                                                                     *
 *                       andreifcoelho@gmail.com                       *
 *                       github.com/andrei-coelho                      *
 ***********************************************************************/
"""

import asyncio
import signal
import pipeline

print("""
    * ██████╗░░█████╗░████████╗░█████╗░███╗░░██╗███████╗██╗░░██╗░█████╗░ *
    * ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗████╗░██║██╔════╝╚██╗██╔╝██╔══██╗ *
    * ██║░░██║███████║░░░██║░░░███████║██╔██╗██║█████╗░░░╚███╔╝░███████║ *
    * ██║░░██║██╔══██║░░░██║░░░██╔══██║██║╚████║██╔══╝░░░██╔██╗░██╔══██║ *
    * ██████╔╝██║░░██║░░░██║░░░██║░░██║██║░╚███║███████╗██╔╝╚██╗██║░░██║ *
    * ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝ *
      
      PIPELINE
      v 0.0.1
""")

parar_loop = asyncio.Event()

async def main():

    def signal_handler(signum, frame):
        print("Sinal recebido, preparando para parar...")
        parar_loop.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not parar_loop.is_set():

        await pipeline.start()
        await asyncio.sleep(10)

    print("Loop interrompido. Encerrando...")


asyncio.run(main())