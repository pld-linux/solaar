Summary:	Linux devices manager for the Logitech Unifying Receiver
Name:		solaar
Version:	0.9.2
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/pwr/Solaar/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2a6ea17150cf030b09ff802cb454358b
URL:		http://pwr.github.io/Solaar/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
Requires:	python-dbus
Requires:	python-pyudev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Solaar is a Linux device manager for Logitech's Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver, and
for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for each
device, and also pair/unpair supported devices with the receiver.

%package gui
Summary:	GUI for Solaar
Group:		X11/Applications
Requires:	python-pygobject
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme

%description gui
Solaar is a Linux device manager for Logitech’s Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver, and
for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for each
device, and also pair/unpair supported devices with the receiver.

%prep
%setup -q -n Solaar-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__python} setup.py \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_icon_cache hicolor

%postun gui
%update_icon_cache hicolor


%files
%defattr(644,root,root,755)
%doc ChangeLog README.md docs/*
%attr(755,root,root) %{_bindir}/solaar-cli
%dir %{py_sitescriptdir}/hidapi
%{py_sitescriptdir}/hidapi/*.py[co]
%dir %{py_sitescriptdir}/logitech_receiver
%{py_sitescriptdir}/logitech_receiver/*.py[co]
%dir %{py_sitescriptdir}/solaar
%{py_sitescriptdir}/solaar/*.py[co]
%exclude %{py_sitescriptdir}/solaar/gtk.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/solaar-0.9.2-py2.7.egg-info
%endif

%files gui
%defattr(644,root,root,755)
/etc/xdg/autostart/solaar.desktop
%attr(755,root,root) %{_bindir}/solaar
%{_datadir}/%{name}
%{_desktopdir}/solaar.desktop
%{_iconsdir}/hicolor/scalable/apps/solaar.svg
%{py_sitescriptdir}/solaar/gtk.py[co]
%dir %{py_sitescriptdir}/solaar/ui
%{py_sitescriptdir}/solaar/ui/*.py[co]
