# todo:
# - PLD backend (now redhat used)
Summary:	Network Manager for GNOME
Name:		NetworkManager
Version:	0.3.1
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	93a3e25b871a1977836b3f778e43b5fe
BuildRequires:	libiw-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager for GNOME.

%prep
%setup -q

%build
%configure --with-distro=redhat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
#%attr(755,root,root) %{_bindir}/*
