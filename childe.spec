# Source1 is not in the repository. ext-rpm.sh makes it on the runner while it
# builds the SRPM, with `cargo vendor --locked` against Cargo.lock, so COPR
# builds offline from the SRPM.

Name:           childe
Version:        0.1.4
Release:        1%{?dist}
Summary:        Utility to open the next empty workspace
# childe is GPL-3.0-or-later (debian/copyright; its Cargo.toml names no
# license, the blank line in the summary). The rest covers the vendored crates:
# update it from the %%{cargo_license_summary} output in the build log whenever
# Cargo.lock changes.
License:        GPL-3.0-or-later AND Apache-2.0 AND BSD-3-Clause AND MIT AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (MIT OR Zlib OR Apache-2.0) AND (Unlicense OR MIT)
URL:            https://github.com/regolith-linux/childe
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  cargo-rpm-macros >= 24

# Not in debian/control: childe reads the workspace name from trawld over
# D-Bus (trawlcat's rescat) and panics when trawld isn't there. The Regolith
# session always runs trawld; this keeps a lone install from crashing.
Requires:       trawld

%description
A window manager utility, meant to be called from a key binding, that
switches to the next empty workspace or moves the focused window there.

%prep
%autosetup -a1
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
%cargo_install

%check
%cargo_test

%files
%license LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}

%changelog
* Thu Nov 05 2026 Regolith Fedora Port <port@regolith.invalid> - 0.1.4-1
- Initial package
