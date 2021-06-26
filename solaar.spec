Summary:	Linux devices manager for the Logitech Unifying Receiver
Name:		solaar
Version:	1.0.6
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/pwr/Solaar/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0b8ba34ae8968a6f4f17d9311f5e54b6
URL:		http://pwr.github.io/Solaar/
BuildRequires:	python3-dbus
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
BuildRequires:	python3-pygobject3
BuildRequires:	python3-pyudev
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.000
Requires:	python3-dbus
Requires:	python3-modules
Requires:	python3-pygobject3
Requires:	python3-pyudev
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Provides:	%{name}-gui = %{version}
Obsoletes:	solaar-gui < %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Solaar is a Linux device manager for Logitech's Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver, and
for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for each
device, and also pair/unpair supported devices with the receiver.

%prep
%setup -q -n Solaar-%{version}

%build
%py3_build

cd tools
sh po-compile.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/udev/rules.d

%py3_install

ln -sr $RPM_BUILD_ROOT%{_bindir}/{%{name},%{name}-cli}

%{__mv} $RPM_BUILD_ROOT%{_datadir}/solaar/udev-rules.d/42-logitech-unify-permissions.rules $RPM_BUILD_ROOT/lib/udev/rules.d/
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/solaar/udev-rules.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%posttrans
# This is needed to apply permissions to existing devices when the package is installed.
/bin/udevadm trigger --subsystem-match=hidraw --action=add

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc ChangeLog docs/*
%attr(755,root,root) %{_bindir}/solaar
%attr(755,root,root) %{_bindir}/solaar-cli
%dir %{py3_sitescriptdir}/hidapi
%{py3_sitescriptdir}/hidapi/*.py
%dir %{py3_sitescriptdir}/hidapi/__pycache__
%{py3_sitescriptdir}/hidapi/__pycache__/*.pyc
%dir %{py3_sitescriptdir}/logitech_receiver
%{py3_sitescriptdir}/logitech_receiver/*.py
%dir %{py3_sitescriptdir}/logitech_receiver/__pycache__
%{py3_sitescriptdir}/logitech_receiver/__pycache__/*.pyc
%dir %{py3_sitescriptdir}/solaar
%{py3_sitescriptdir}/solaar/*.py
%dir %{py3_sitescriptdir}/solaar/__pycache__
%{py3_sitescriptdir}/solaar/__pycache__/*.pyc
%dir %{py3_sitescriptdir}/solaar/cli
%{py3_sitescriptdir}/solaar/cli/*.py
%dir %{py3_sitescriptdir}/solaar/cli/__pycache__
%{py3_sitescriptdir}/solaar/cli/__pycache__/*.pyc
%dir %{py3_sitescriptdir}/solaar/ui
%{py3_sitescriptdir}/solaar/ui/*.py
%dir %{py3_sitescriptdir}/solaar/ui/__pycache__
%{py3_sitescriptdir}/solaar/ui/__pycache__/*.pyc
%{py3_sitescriptdir}/solaar-%{version}-py%{py3_ver}.egg-info
%{_datadir}/%{name}
%{_desktopdir}/solaar.desktop
%{_iconsdir}/hicolor/scalable/apps/solaar.svg
%{_datadir}/metainfo/io.github.pwr_solaar.solaar.metainfo.xml
%{_localedir}/*/LC_MESSAGES/%{name}.mo
/lib/udev/rules.d/42-logitech-unify-permissions.rules
