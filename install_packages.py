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
            BrewRecipeInstaller("ansible"),
            StandardInstaller(
                    command = "autojump",
                    install_cmd  = "brew install autojump",
                    profile_additions = [
                        """[ -f /opt/homebrew/etc/profile.d/autojump.sh ] && . /opt/homebrew/etc/profile.d/autojump.sh""" 
                    ],
            ),
            StandardInstaller( command = "uv",
                install_cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh",
            ),
            StandardInstaller(
                command = "gimme",
                install_cmd = "mkdir -p ~/bin; curl -sL -o ~/bin/gimme https://raw.githubusercontent.com/travis-ci/gimme/master/gimme; chmod +x ~/bin/gimme; gimme 1.24.0",
                profile_additions = [
                    """source ~/.gimme/envs/latest.env"""
                ]
            ),
            PromptInstaller(),
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
        raise Exception("not implemented")

    def name(self) -> str:
        """the name of the installer"""
        raise Exception("not implemented")

    async def install(self):
        """may throw an InstallError"""
        raise Exception("not implemented")


class InstallError(Exception):
    def __init__(self, msg):
        super().__init__(self)
        self.msg = msg



class StandardInstaller(Installer):

    def __init__(
            self,
            command,
            install_cmd,
            profile_additions = None,
    ):
        self.command = command
        self.install_cmd = install_cmd
        self.profile_additions = profile_additions


    def name(self) -> str:
        return self.command

    async def is_installed(self):
        return await is_installed(self.command)

    async def install(self):
        await run_command(["zsh", "-c", "source ~/.zprofile; " + self.install_cmd])

        if self.profile_additions != None and len(self.profile_additions) > 0:
            await add_block(self.command, "\n".join(self.profile_additions), zprofile_path())


class BrewRecipeInstaller(StandardInstaller):

    def __init__(self, name):
        super().__init__(
                command = name,
                install_cmd = "brew install " + name,
        )

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
        check_file = Path.home().joinpath(".nvm/nvm.sh")
        return await file_exists(check_file)
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


class PromptInstaller(Installer):
    def name(self) -> str:
        return "custom prompt"
    async def is_installed(self):
        return False # TODO

    async def install(self):
        await run_command(["zsh", "-c", "mkdir -p ~/code; cd ~/code; git clone git@github.com:leeavital/lees-prompt.git"])
        await run_command(["zsh", "-c", "cd ~/code/lees-prompt; cargo build"])
        await run_command(["zsh", "-c", "mv  ~/code/lees-prompt/target/debug/prompt ~/bin/prompt"])






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

async def file_exists(path):
    import aiofiles.os
    return await aiofiles.os.path.exists(path)


def zprofile_path():
    return Path.home().joinpath(".zprofile")

asyncio.run(main())
