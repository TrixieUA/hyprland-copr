Name:           hyprland
Version:        0.29.0
Release:        %autorelease.nvidia
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

# main source code is BSD-3-Clause
# subprojects/hyprland-protocols is BSD-3-Clause
# subprojects/wlroots is MIT
# subproject/udis86 is BSD-2-Clause
License:        BSD-3-Clause AND MIT AND BSD-2-Clause
URL:            https://github.com/hyprwm/Hyprland
Source:         %{url}/releases/download/v%{version}/source-v%{version}.tar.gz

# Revert passing git information to meson to avoid a build requirment on git.
# https://github.com/hyprwm/Hyprland/commit/0eebf3ab1614a34433cc4d208be84b930b88e25c
Patch:          0001-Partially-revert-meson-add-DGIT-arguments-321.patch

# The dependency is optional, and xcb-errors is not yet packaged in Fedora.
# The system wlroots disables this dependency as well.
Patch:          0002-Disable-xcb-errors-in-bundled-wlroots.patch
Patch:		nvidia.patch

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  jq

# dependencies found by running:
# grep --recursive --include meson.build dependency

# meson.build
BuildRequires:  pkgconfig(xcb)
BuildRequires:  cmake
BuildRequires:  pkgconfig(libsystemd)
# protocols/meson.build
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
# src/meson.build
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
# subprojects/wlroots/meson.build
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pixman-1)
# subprojects/wlroots/backend/drm/meson.build
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libliftoff)
# subprojects/wlroots/backend/libinput/meson.build
BuildRequires:  pkgconfig(libinput)
# subprojects/wlroots/backend/session/meson.build
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libseat)
# subprojects/wlroots/backend/wayland/meson.build
BuildRequires:  pkgconfig(wayland-client)
# subprojects/wlroots/backend/x11/meson.build
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
# subprojects/wlroots/protocol/meson.build
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
# subprojects/wlroots/render/meson.build
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
# subprojects/wlroots/render/allocator/meson.build
BuildRequires:  pkgconfig(gbm)
# subprojects/wlroots/render/gles2/meson.build
BuildRequires:  pkgconfig(glesv2)
# subprojects/wlroots/render/pixman/meson.build
BuildRequires:  pkgconfig(pixman-1)
# subprojects/wlroots/render/vulkan/meson.build
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  glslang
# subprojects/wlroots/xwayland/meson.build
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  clang

# Upstream insists on always building against very current snapshots of
# wlroots, and doesn't provide a method for building against a system copy.
# https://github.com/hyprwm/Hyprland/issues/302
Provides:       bundled(wlroots) = 0.17.0~^1.7abda95

# Currently this library is only used by hyprland, so we'll keep it bundled for
# now until something else needs it as a system package.
Provides:       bundled(hyprland-protocols) = 0.1^1.d7d403b

# udis86 is packaged in Fedora, but the copy bundled here is actually a
# modified fork.
Provides:       bundled(udis86) = 1.7.2^1.5336633


%description
Hyprland is a dynamic tiling Wayland compositor based on wlroots that doesn't
sacrifice on its looks.  It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful plugin
system and more. 


%prep
%autosetup -p 1 -n hyprland-source
cp subprojects/hyprland-protocols/LICENSE LICENSE-hyprland-protocols
cp subprojects/udis86/LICENSE LICENSE-udis86
cp subprojects/wlroots/LICENSE LICENSE-wlroots


%build
%meson
%meson_build


%install
%meson_install

# remove wlroots development files
rm -r %{buildroot}%{_includedir}/wlr
rm -r %{buildroot}%{_libdir}/libwlroots.a
rm -r %{buildroot}%{_libdir}/pkgconfig/wlroots.pc

# remove hyprland-protocols development files
rm %{buildroot}%{_datadir}/pkgconfig/hyprland-protocols.pc      


%files
%license LICENSE LICENSE-hyprland-protocols LICENSE-udis86 LICENSE-wlroots
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{_datadir}/hyprland
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/hyprland-protocols
%{_datadir}/pkgconfig
%{_datadir}/xdg-desktop-portal
%{_includedir}/hyprland


%changelog
%autochangelog
