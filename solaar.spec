Summary:	Linux devices manager for the Logitech Unifying Receiver
Summary(pl.UTF-8):	Linuksowy menedżer urządzeń dedykowany zunifikowanym odbiornikom firmy Logitech
Name:		solaar
Version:	1.1.5
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/pwr-Solaar/Solaar/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	96960256536d4538f2b9e9fa390dee71
URL:		https://pwr-solaar.github.io/Solaar/
BuildRequires:	gettext-tools
BuildRequires:	python3-dbus
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

%description -l pl.UTF-8
Solarar to menedżer urządzeń dla systemu Linux dla urządzeń
peryferyjnych będących zunifikowanymi odbiornikami firmy Logitech.
Solaar Jest w stanie sparować/rozparować urządzenia z odbiornikiem, a
dla większości urządzeń również odczytać stan baterii.

Występuje w dwóch wersjach: wiersza poleceń i GUI. Oba są w stanie
wyświetlić listę urządzeń sparowanych z odbiornikiem, wyświetlić
szczegółowe informacje o każdym urządzeniu, a także
sparować/rozparować obsługiwane urządzenia z odbiornikiem.

%prep
%setup -q -n Solaar-%{version}

%build
%py3_build
sh tools/po-compile.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/xdg/autostart/
install -d $RPM_BUILD_ROOT/lib/udev/rules.d
%{__sed} -i '1s,%{_bindir}/env python3,%{__python3},' tools/hidconsole

%py3_install

ln -sr $RPM_BUILD_ROOT%{_bindir}/{%{name},%{name}-cli}
install -pm755 tools/hidconsole $RPM_BUILD_ROOT%{_bindir}
install -pm644 share/autostart/solaar.desktop $RPM_BUILD_ROOT/etc/xdg/autostart/
%{__mv} $RPM_BUILD_ROOT%{_datadir}/solaar/udev-rules.d/42-logitech-unify-permissions.rules $RPM_BUILD_ROOT/lib/udev/rules.d/
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/solaar/udev-rules.d
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/rs
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%posttrans
# This is needed to apply permissions to existing devices when the package is installed.
/bin/udevadm trigger --subsystem-match=hidraw --action=add

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog.md docs/*
%attr(755,root,root) %{_bindir}/hidconsole
%attr(755,root,root) %{_bindir}/solaar
%attr(755,root,root) %{_bindir}/solaar-cli
/etc/xdg/autostart/solaar.desktop
%dir %{py3_sitescriptdir}/hidapi
%{py3_sitescriptdir}/hidapi/*.py
%dir %{py3_sitescriptdir}/hidapi/__pycache__
%{py3_sitescriptdir}/hidapi/__pycache__/*.pyc
%dir %{py3_sitescriptdir}/keysyms
%{py3_sitescriptdir}/keysyms/*.py
%dir %{py3_sitescriptdir}/keysyms/__pycache__
%{py3_sitescriptdir}/keysyms/__pycache__/*.pyc
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
/lib/udev/rules.d/42-logitech-unify-permissions.rules
