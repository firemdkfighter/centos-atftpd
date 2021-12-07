Summary: Advanced TFTP Server and Client
Name: atftp
Version: 0.7.5
Release: 1%{?dist}
Group:  System/Daemons
License: GPL

Url: https://sourceforge.net/projects/atftp/
Source0: https://downloads.sf.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1: https://raw.githubusercontent.com/archlinux/svntogit-community/packages/atftp/trunk/atftpd.conf
Source2: https://raw.githubusercontent.com/archlinux/svntogit-community/packages/atftp/trunk/atftpd.service
Source3: https://raw.githubusercontent.com/archlinux/svntogit-community/packages/atftp/trunk/sysusers.conf
Source4: https://raw.githubusercontent.com/archlinux/svntogit-community/packages/atftp/trunk/tmpfiles.conf

Requires: pcre readline
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

Provides:       tftp(client)
Provides:       tftp(server)

%description
Client/server implementation of the TFTP protocol that implements RFCs 1350, 2090, 2347, 2348, and 2349

%prep
%setup -q

%build
CFLAGS+=' -std=gnu89'

./configure \
  --prefix=/usr \
  --mandir=/usr/share/man \
  --sbindir=/usr/bin \
  --enable-libreadline \
  --disable-libwrap
make

%install
%make_install
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/conf.d/atftpd
install -D -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/atftpd.service
install -D -m 0644 %{SOURCE3} %{buildroot}/%{_sysusersdir}/atftp.conf
install -D -m 0644 %{SOURCE4} %{buildroot}/%{_tmpfilesdir}/atftp.conf

%files
%config %{_sysconfdir}/conf.d/atftpd
%{_unitdir}/atftpd.service
%{_sysusersdir}/atftp.conf
%{_tmpfilesdir}/atftp.conf
%{_bindir}/atftp
%{_bindir}/atftpd
%{_bindir}/in.tftpd
%{_mandir}/*/atftp*
%{_mandir}/man8/in.tftpd.8.gz

%post
%systemd_post atftpd.service

%preun
%systemd_preun atftpd.service

%postun
%systemd_postun_with_restart atftpd.service
