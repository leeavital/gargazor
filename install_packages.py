#!/usr/bin/env python3

import asyncio
import subprocess
import aiofiles
import os
from pathlib import Path
from rich.console import Console

async def main():

    console = Console()

    # await DMGInstaller("VSCode", "https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal").install()
    installers = [
            NVMInstaller(),
            CargoBinstallInstaller(),
            RustInstaller(),
            BrewRecipeInstaller("jj"),
    ]

    for i in installers:
        if await i.is_installed():
            console.log(f"[bold green]{i.name()} is already installed[/bold green]")
            continue

        with console.status(f"[bold green]installing {i.name()}[/bold green]"):
            try:
                await i.install()
                console.log(f"[bold green]installed {i.name()}![/bold green]")
            except InstallError as e:
                console.log(f"[bold red]could not install {i.name()}[/bold red]")
                console.log(f"[italic red]{e.msg}[/italic red]")

class Installer:
    async def is_installed(self) -> bool:
        pass

    def name(self) -> str:
        """the name of the installer"""
        pass

    async def install(self):
        """may throw an InstallError"""
        pass


class InstallError(Exception):
    def __init__(self, msg):
        super().__init__(self)
        self.msg = msg


class BrewRecipeInstaller(Installer):

    def __init__(self, name):
        self._name = name

    async def is_installed(self) -> bool:
        return await is_installed("jj")

    def name(self) -> str:
        return "brew " + self._name

    async def install(self):
        await run_command(["brew", "install", self.name])

class CargoBinstallInstaller(Installer):

    async def is_installed(self) -> bool:
        return await is_installed("cargo-binstall")

    def name(self):
        return "cargo-binstall"

    async def install(self):
        out = await run_command(["brew", "install", "cargo-binstall"])
        print(out)
        contents = """
        . "$HOME/.cargo/env"
        """
        await add_block("cargo-install", contents, zprofile_path())


class NVMInstaller(Installer):
    def name(self) -> str:
        return "nvm"
    async def is_installed(self):
        return await is_installed("nvm")
    async def install(self):
        out = await run_command(["bash", "-c", "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"])

        content = """
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion"""
        await add_block("nvm", content, zprofile_path())


        out = await run_command(["zsh", "-c", "source ~/.zprofile; nvm install --lts"])

class RustInstaller(Installer):
    def name(self) -> str:
        return "rustc"
    async def is_installed(self):
        return await is_installed("rustc")
    async def install(self):
        out = await run_command(["zsh", "-c", "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"])

        contents = """
        . "$HOME/.cargo/env"
        """
        await add_block("rustup", contents, zprofile_path())




async def is_installed(cmd):
    check = f"source ~/.zprofile; which {cmd}"
    proc = await asyncio.create_subprocess_exec("bash", "-c", check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await proc.communicate()
    return proc.returncode == 0


async def run_command(parts):
    (r, w) = os.pipe()

    async with aiofiles.open(w, mode='w') as interleaved:
        proc = await asyncio.create_subprocess_exec(*parts, stdin=subprocess.PIPE, stdout=interleaved, stderr=interleaved)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        async with aiofiles.open(r, mode='r') as interleaved:
            stderr = "".join([l for l in await interleaved.readlines()])
            raise InstallError(stderr)
    return stdout


async def add_block(slug, target_content, filename="~/.zprofile"):
    async with aiofiles.open(filename, mode='r') as f:
        contents = (await f.read()).split("\n")

    start = "###### BEGIN " + slug + " #######"
    end = "###### END " + slug + " #######"

    try:
        startIndex = contents.index(start)
        endIndex = contents.index(end)
    except ValueError:
        startIndex = None
        endIndex = None


    if startIndex == None:
        contents.extend([start, target_content, end])
    else:
        contents = contents[0:startIndex + 1] + [target_content] + contents[endIndex:]

    new_contents = "\n".join(contents)

    async with aiofiles.open(filename, mode='w') as f:
        await f.write(new_contents)


def zprofile_path():
    return Path.home().joinpath(".zprofile")

asyncio.run(main())
