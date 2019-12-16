%define debug_package %{nil}
Name:          gnu-efi
Version:       3.0.8
Release:       3
Summary:       Development Libraries and headers for EFI
Epoch:         1
License:       BSD
URL:           ftp://ftp.hpl.hp.com/pub/linux-ia64
ExclusiveArch: x86_64 aarch64
Source:        http://superb-dca2.dl.sourceforge.net/project/gnu-efi/gnu-efi-3.0.6.tar.bz2
#stubs-32.h comes from http://www.gnu.org/software/glibc/
Source1:       stubs-32.h

Patch0001:     0001-PATCH-Disable-AVX-instruction-set-on-IA32-and-x86_64.patch
Patch0002:     0002-Use-ARFLAGS-when-invoking-ar.patch
Patch0003:     0003-Stripped-diff-for-makefile.patch
Patch0004:     0004-Make-sure-stdint.h-is-always-used-with-MSVC-on-ARM-A.patch
Patch0005:     0005-Add-EFI_DRIVER_ENTRY_POINT-support-for-MSVC-ARM64.patch
Patch0006:     0006-Move-memcpy-memset-definition-to-global-init.c.patch
Patch0007:     0007-Bump-revision-from-VERSION-3.0.6-to-VERSION-3.0.7.patch
Patch0008:     0008-Currently-we-have-DivU64x32-on-ia32-but-it-tries-to-.patch
Patch0009:     0009-gnuefi-preserve-.gnu.hash-sections-unbreaks-elilo-on.patch
Patch0010:     0010-gnu-efi-fix-lib-ia64-setjmp.S-IA-64-build-failure.patch
Patch0011:     0011-Fix-some-types-gcc-doesn-t-like.patch
Patch0012:     0012-Fix-arm-build-paths-in-the-makefile.patch
Patch0013:     0013-Work-around-Werror-maybe-uninitialized-not-being-ver.patch
Patch0014:     0014-Fix-a-sign-error-in-the-debughook-example-app.patch
Patch0015:     0015-Fix-typedef-of-EFI_PXE_BASE_CODE.patch
Patch0016:     0016-make-clang-not-complain-about-fno-merge-all-constant.patch
Patch0017:     0017-Fix-another-place-clang-complains-about.patch
Patch0018:     0018-gnu-efi-add-some-more-common-string-functions.patch
Patch0019:     0019-Add-D-to-print-device-paths.patch
Patch0020:     0020-Make-ARCH-overrideable-on-the-command-line.patch
Patch0021:     0021-apps-Add-bltgrid-and-lfbgrid-and-add-error-checks-to.patch
Patch0022:     0022-Nerf-Werror-pragma-away.patch
Patch0023:     0023-Call-ar-in-deterministic-mode.patch
Patch0024:     0024-Add-debug-helper-applications.patch
Patch0025:     0025-Bump-revision-from-VERSION-3.0.7-to-VERSION-3.0.8.patch

Patch9000:     stubs-32-h.patch

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
%autosetup  -n gnu-efi-3.0.6 -p1

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
* Wed Nov 20 2019 yangjian<yangjian79@huawei.com> - 3.0.8-3
- Package init
