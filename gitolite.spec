%define gl_datadir %{_datadir}/%{name}
%define gl_homedir %{_sharedstatedir}/%{name}

Name:           gitolite
Summary:        Git hosting tool
Version:        3.6.7
Release:        3
License:        GPLv2
Group:          Development/Other
URL:            http://sitaramc.github.com/gitolite/
Source0:        https://github.com/sitaramc/gitolite/archive/v%{version}/%{name}-%{version}.tar.gz
# Upstream: https://github.com/sitaramc/gitolite/commit/c656af01b73a5cc4f80512
Source1:        compile-1
# From Fedora: https://src.fedoraproject.org/rpms/gitolite3/blob/master/f/gitolite3-README-fedora
Source2:        gitolite-README-fedora
# From upstream: reduce stat() and other expensive calls on large installs
Patch0:         https://github.com/sitaramc/gitolite/commit/41b7885b77.patch
# From upstream: allow orphan gl-conf files
Patch1:         https://github.com/sitaramc/gitolite/commit/c4b6521a4b.patch

# For rpm-helper macros
BuildRequires:  rpm-helper

# For runtime usage of rpm-helper
Requires(pre):  rpm-helper

BuildArch:      noarch

%description
Gitolite allows you to setup git hosting on a central server, with
fine-grained access control and many more powerful features.

%prep
%autosetup -p1

cp %{SOURCE2} .

%build
# Nothing to build

%install
# Directories
install -d %{buildroot}%{gl_homedir}
install -d %{buildroot}%{gl_homedir}/.ssh
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{perl_vendorlib}
install -d %{buildroot}%{gl_datadir}

# Code
cp -a src/lib/Gitolite %{buildroot}%{perl_vendorlib}
echo "%{version}-%{release}" > src/VERSION
cp -a src/* %{buildroot}%{gl_datadir}
cp %{SOURCE1} %{buildroot}%{gl_datadir}/commands/

install -D -m755 check-g2-compat %{buildroot}%{_bindir}/check-g2-compat
install -D -m755 convert-gitosis-conf %{buildroot}%{_bindir}/convert-gitosis-conf
ln -sr %{buildroot}%{gl_datadir}/gitolite %{buildroot}%{_bindir}/gitolite

# empty authorized_keys file
touch %{buildroot}%{gl_homedir}/.ssh/authorized_keys

%pre
%_pre_useradd %{name} %{gl_homedir} /bin/sh

%postun
%_postun_userdel %{name}

%files
%doc CHANGELOG README.markdown gitolite-README-fedora
%license COPYING
%{_bindir}/gitolite
%{_bindir}/check-g2-compat
%{_bindir}/convert-gitosis-conf
%{perl_vendorlib}/*
%{gl_datadir}
# Make homedir non-world readable
%attr(750,%{name},%{name}) %dir %{gl_homedir}
%attr(750,%{name},%{name}) %dir %{gl_homedir}/.ssh
%config(noreplace) %attr(640,%{name},%{name}) %{gl_homedir}/.ssh/authorized_keys
