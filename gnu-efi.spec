%define debug_package %{nil}
Name:          gnu-efi
Version:       3.0.8
Release:       5
Summary:       Development Libraries and headers for EFI
Epoch:         1
License:       BSD
URL:           ftp://ftp.hpl.hp.com/pub/linux-ia64
ExclusiveArch: x86_64 aarch64
Source:        http://superb-dca2.dl.sourceforge.net/project/gnu-efi/gnu-efi-3.0.8.tar.bz2
#stubs-32.h comes from http://www.gnu.org/software/glibc/
Source1:       stubs-32.h

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed  's/^ID=//'))

%ifarch x86_64
%global efiarch x86_64
%endif
%ifarch aarch64
%global efiarch aarch64
%endif

Provides:  %{name}-utils = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-utils < %{epoch}:%{version}-%{release}

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%package devel
Summary:   Development Libraries and headers for EFI
Obsoletes: gnu-efi < 1:3.0.2-1
Requires:  gnu-efi

%description devel
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup  -n gnu-efi-3.0.8 -p1
install -d gnuefi/gnu
install -Dp %{SOURCE1} gnuefi/gnu/

%build
make
make apps
%ifarch x86_64
setarch linux32 -B make ARCH=ia32 PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib
setarch linux32 -B make ARCH=ia32 PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib apps
%endif

%install
install -d %{buildroot}/%{_libdir}/gnuefi
install -d %{buildroot}/boot/efi/EFI/%{efidir}/%{efiarch}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install
mv %{buildroot}/%{_libdir}/*.lds %{buildroot}/%{_libdir}/*.o %{buildroot}/%{_libdir}/gnuefi
mv %{efiarch}/apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/%{efidir}/%{efiarch}/

%ifarch x86_64
install -d %{buildroot}/%{_prefix}/lib/gnuefi
install -d %{buildroot}/boot/efi/EFI/%{efidir}/ia32

setarch linux32 -B make PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib INSTALLROOT=%{buildroot} ARCH=ia32 install
mv %{buildroot}/%{_prefix}/lib/*.{lds,o} %{buildroot}/%{_prefix}/lib/gnuefi/
mv ia32/apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/%{efidir}/ia32/
%endif

%files
%{_prefix}/lib*/*
%dir %attr(0700,root,root) /boot/efi/EFI/%{efidir}/*/
%attr(0700,root,root) /boot/efi/EFI/%{efidir}/*/*.efi

%files devel
%defattr(-,root,root,-)
%doc README.* ChangeLog
%{_includedir}/efi

%changelog
* Fri Mar 13 2020 zhujunhao<zhujunhao5@huawei.com> - 3.0.8-5
- Modify x86 build failed

* Wed Jan 15 2020 yuxiangyang4<yuxiangyang4@huawei.com> - 3.0.8-4
- Upgrade source code to 3.0.8

* Wed Nov 20 2019 yangjian<yangjian79@huawei.com> - 3.0.8-3
- Package init
